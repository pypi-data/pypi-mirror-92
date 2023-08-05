from typing import Dict, List
from enum import Enum
from collections import namedtuple

from arrowhead_client.system import ArrowheadSystem
from arrowhead_client.service import Service, ServiceInterface
from arrowhead_client.rules import OrchestrationRule
from arrowhead_client.common import Constants

CoreConfig = namedtuple(
        'CoreConfig',
        ['service_definition',
         'uri',
         'method',
         'protocol',
         'payload',
         'system',
         ]
)


class CoreServices(CoreConfig, Enum):
    # Core services
    SERVICE_REGISTER = (
        'service-register',
        'serviceregistry/register',
        'POST', 'HTTP', 'JSON',
        Constants.CORE_SYSTEM_SERVICE_REGISTRY.value,
    )
    SERVICE_UNREGISTER = (
        'service-unregister',
        'serviceregistry/unregister',
        'DELETE', 'HTTP', 'JSON',
        Constants.CORE_SYSTEM_SERVICE_REGISTRY.value,
    )
    SERVICE_QUERY = (
        'service-query',
        'serviceregistry/query',
        'POST', 'HTTP', 'JSON',
        Constants.CORE_SYSTEM_SERVICE_REGISTRY.value,
    )
    ORCHESTRATION = (
        'orchestration-service',
        'orchestrator/orchestration',
        'POST', 'HTTP', 'JSON',
        Constants.CORE_SYSTEM_ORCHESTRATOR.value,
    )
    PUBLICKEY = (
        'auth-public-key',
        'authorization/publickey',
        'GET', 'HTTP', 'JSON',
        Constants.CORE_SYSTEM_AUTHORIZATION.value,
    )


def get_core_rules(config: Dict, secure: bool) -> List[OrchestrationRule]:
    """
    Get orchestration rules for core services.

    Args:
        config: Configuration dictionary.
        secure: True if ssl is enabled, False otherwise.
    Returns:
        List of Orchestration rules.
    """

    rules = [_extract_rule(core_service, config, secure)
             for core_service in CoreServices]

    return rules


def _extract_rule(core_service_tuple, config, secure) -> OrchestrationRule:
    secure = Constants.SECURITY_SECURE if secure else Constants.SECURITY_INSECURE
    access_policy = Constants.POLICY_CERTIFICATE if secure else Constants.POLICY_UNRESTRICTED
    interface = ServiceInterface(core_service_tuple.protocol, secure, core_service_tuple.payload)
    core_system = ArrowheadSystem(**config[core_service_tuple.system])
    return OrchestrationRule(
            Service(
                    core_service_tuple.service_definition,
                    core_service_tuple.uri,
                    interface,
                    access_policy,
            ),
            core_system,
            core_service_tuple.method,
    )
