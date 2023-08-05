from __future__ import annotations

from functools import partial
from typing import Any, Dict, Tuple, Callable

from arrowhead_client.system import ArrowheadSystem
from arrowhead_client.abc import BaseConsumer, BaseProvider
from arrowhead_client.service import Service, ServiceInterface
from arrowhead_client.client.core_services import get_core_rules, CoreServices
from arrowhead_client.client import (
    core_service_responses as responses,
    core_service_forms as forms
)
from arrowhead_client.client.core_system_defaults import config as ar_config
from arrowhead_client.security.access_policy import get_access_policy
from arrowhead_client.common import Constants
from arrowhead_client.rules import (
    OrchestrationRuleContainer,
    RegistrationRuleContainer,
    RegistrationRule,
)
import arrowhead_client.errors as errors

def provided_service(
            service_definition: str,
            service_uri: str,
            protocol: str,
            method: str,
            payload_format: str,
            access_policy: str,
    ):
    """
    Decorator that can be used in custom client subclasses to define services.

    Args:
        service_definition:
        service_uri:
        protocol:
        method:
        payload_format:
        access_policy:

    Returns:
        A ServiceDescriptor object
    """

    class ServiceDescriptor:
        def __init__(self, func):
            self.service_instance = Service(
                    service_definition,
                    service_uri,
                    ServiceInterface.with_access_policy(
                            protocol,
                            access_policy,
                            payload_format,
                    ),
                    access_policy,
            )
            self.method = method
            self.service_definition = service_definition
            self.func = func

        def __set_name__(self, owner: ArrowheadClient, name: str):
            if not '__arrowhead_services__' in dir(owner):
                raise AttributeError(f'provided_service can only be used within arrowhead clients.')

            owner.__arrowhead_services__.append(name)

        def __get__(self, instance, owner):
            if instance is None:
                return self

            return RegistrationRule(
                    provided_service=self.service_instance,
                    provider_system=instance.system,
                    method=self.method,
                    func=partial(self.func, instance),
            )

    return ServiceDescriptor

class ArrowheadClient:
    """
    Application class for Arrowhead Systems.

    This class serves as a bridge that connects systems, consumers, and providers to the user.

    Attributes:
        system: ArrowheadSystem
        consumer: Consumer
        provider: Provider
        logger: Logger, will default to the logger found in logs.get_logger()
        keyfile: PEM keyfile
        certfile: PEM certfile
    """

    def __init__(self,
                 system: ArrowheadSystem,
                 consumer: BaseConsumer,
                 provider: BaseProvider,
                 logger: Any,
                 config: Dict = None,
                 keyfile: str = '',
                 certfile: str = '', ):
        self.system = system
        self.consumer = consumer
        self.provider = provider
        self.keyfile = keyfile
        self.certfile = certfile
        self.secure = all(self.cert)
        self._logger = logger
        self.config = config or ar_config
        self.auth_authentication_info = None
        self.orchestration_rules = OrchestrationRuleContainer()
        self.registration_rules = RegistrationRuleContainer()
        # TODO: Should add_provided_service be exactly the same as the provider's,
        # or should this class do something on top of it?
        # It's currently not even being used so it could likely be removed.
        # Maybe it should be it's own method?
        self.add_provided_service = self.provider.add_provided_service

    __arrowhead_services__ = []

    @property
    def cert(self) -> Tuple[str, str]:
        """ Tuple of the keyfile and certfile """
        return self.certfile, self.keyfile

    def setup(self):
        # Setup methods
        self._core_service_setup()

        for class_service_rule in self.__arrowhead_services__:
            self.registration_rules.store(getattr(self, class_service_rule))

    def consume_service(
            self,
            service_definition: str,
            **kwargs
    ):
        """
        Consumes the given provided_service definition

        Args:
            service_definition: The provided_service definition of a consumable provided_service
            **kwargs: Collection of keyword arguments passed to the consumer.
        """

        rule = self.orchestration_rules.get(service_definition)
        if rule is None:
            # TODO: Not sure if this should raise an error or just log?
            raise errors.NoAvailableServicesError(
                    f'No services available for'
                    f' service \'{service_definition}\''
            )

        return self.consumer.consume_service(rule, **kwargs, )

    def add_orchestration_rule(
            self,
            service_definition: str,
            method: str,
            protocol: str = '',
            access_policy: str = '',
            format: str = '',
            # TODO: Should **kwargs just be orchestration_flags and preferred_providers?
            **kwargs,
    ) -> None:
        """
        Add orchestration rule for provided_service definition

        Args:
            service_definition: Service definition that is looked up from the orchestrator.
            method: The HTTP method given in uppercase that is used to consume the provided_service.
            access_policy: Service access policy.
        """

        requested_service = Service(
                service_definition,
                interface=ServiceInterface.with_access_policy(
                        protocol,
                        access_policy,
                        format,
                ),
                access_policy=access_policy
        )

        orchestration_form = forms.OrchestrationForm.make(
                self.system,
                requested_service,
                **kwargs
        )

        orchestration_response = self.consume_service(
                CoreServices.ORCHESTRATION.service_definition,
                json=orchestration_form.dto(),
                cert=self.cert,
        )

        rules = responses.process_orchestration(orchestration_response, method)

        for rule in rules:
            self.orchestration_rules.store(rule)

    def provided_service(
            self,
            service_definition: str,
            service_uri: str,
            protocol: str,
            method: str,
            payload_format: str,
            access_policy: str,
    ) -> Callable:
        """
        Decorator to add a provided provided_service to the provider.

        Args:
            service_definition: Service definition to be stored in the provided_service registry
            service_uri: The path to the provided_service
            method: HTTP method required to access the provided_service
        """

        provided_service = Service(
                service_definition,
                service_uri,
                ServiceInterface.with_access_policy(
                        protocol,
                        access_policy,
                        payload_format,
                ),
                access_policy,
        )

        def wrapped_func(func):
            self.registration_rules.store(
                    RegistrationRule(
                            provided_service,
                            self.system,
                            method,
                            func,
                    )
            )
            return func

        return wrapped_func

    def run_forever(self) -> None:
        """
        Start the server, publish all provided_service, and run until interrupted.
        Then, unregister all services.
        """

        try:
            self.setup()
            # TODO: These three could go into a provider_setup() method
            if self.secure:
                authorization_response = self.consume_service(CoreServices.PUBLICKEY.service_definition)
                self.auth_authentication_info = responses.process_publickey(authorization_response)
            self._initialize_provided_services()
            self._register_all_services()
            self._logger.info('Starting server')
            print('Started Arrowhead ArrowheadSystem')
            self.provider.run_forever(
                    address=self.system.address,
                    port=self.system.port,
                    # TODO: keyfile and certfile should be given in provider.__init__
                    keyfile=self.keyfile,
                    certfile=self.certfile,
            )
        except KeyboardInterrupt:
            self._logger.info('Shutting down server')
        finally:
            print('Shutting down Arrowhead system')
            self._unregister_all_services()
            self._logger.info('Server shut down')

    def _initialize_provided_services(self) -> None:
        for rule in self.registration_rules:
            rule.access_policy = get_access_policy(
                    policy_name=rule.provided_service.access_policy,
                    provided_service=rule.provided_service,
                    privatekey=self.keyfile,
                    authorization_key=self.auth_authentication_info
            )
            self.provider.add_provided_service(rule)

    def _core_service_setup(self) -> None:
        """
        Method that sets up the test_core services.

        Runs when the client is created and should not be run manually.
        """

        core_rules = get_core_rules(self.config, self.secure)

        for rule in core_rules:
            self.orchestration_rules.store(rule)

    def _register_service(self, service: Service):
        """
        Registers the given provided_service with provided_service registry

        Args:
            service: Service to register with the Service registry.
        """

        service_registration_form = forms.ServiceRegistrationForm.make(
                provided_service=service,
                provider_system=self.system,
        )

        service_registration_response = self.consume_service(
                CoreServices.SERVICE_REGISTER.service_definition,
                json=service_registration_form.dto(),
                cert=self.cert
        )

        responses.process_service_register(
                service_registration_response,
        )

    def _register_all_services(self) -> None:
        """
        Registers all provided services of the system with the system registry.
        """
        for rule in self.registration_rules:
            try:
                self._register_service(rule.provided_service)
            except errors.CoreServiceInputError as e:
                # TODO: Do logging
                print(e)
            else:
                rule.is_provided = True

    def _unregister_service(self, service: Service) -> None:
        """
        Unregisters the given provided_service with provided_service registry

        Args:
            service: Service to unregister with the Service registry.
        """

        service_definition = service.service_definition

        # TODO: Should be a "form"?
        unregistration_payload = {
            'service_definition': service_definition,
            'system_name': self.system.system_name,
            'address': self.system.address,
            'port': self.system.port
        }

        service_unregistration_response = self.consume_service(
                CoreServices.SERVICE_UNREGISTER.service_definition,
                params=unregistration_payload,
                cert=self.cert
        )

        responses.process_service_unregister(service_unregistration_response)

    def _unregister_all_services(self) -> None:
        """
        Unregisters all provided services of the system with the system registry.
        """

        for rule in self.registration_rules:
            if not rule.is_provided:
                continue
            try:
                self._unregister_service(rule.provided_service)
            except errors.CoreServiceInputError as e:
                print(e)
            else:
                rule.is_provided = False
