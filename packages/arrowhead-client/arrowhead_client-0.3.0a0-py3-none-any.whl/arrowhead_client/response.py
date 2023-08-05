from typing import Union, Dict
from dataclasses import dataclass
import json

from arrowhead_client.common import Constants


@dataclass
class Response:
    """
    Class for storing responses from systems
    """
    payload: bytes
    payload_type: str
    status_code: Union[str, int]

    def read_json(self) -> Dict:
        if self.payload_type != Constants.PAYLOAD_JSON:
            raise RuntimeError(f'Payload type must be \'{Constants.PAYLOAD_JSON}\' to use read_json(), '
                               f'current type is {self.payload_type}')

        try:
            return json.loads(self.payload)
        except json.JSONDecodeError as e:
            raise RuntimeError(f'Payload of type \'{Constants.PAYLOAD_JSON}\' '
                               f'is unable to be decoded. Current payload is:\n'
                               f' {self.payload.decode()}') from e

    def read_string(self) -> str:
        return self.payload.decode()
