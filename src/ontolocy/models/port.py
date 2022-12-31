from enum import Enum
from typing import Any, ClassVar, Dict, Optional
from uuid import UUID

from pydantic import validator

from ..node import OntolocyNode
from ..utils import generate_deterministic_uuid


class PortProtocolEnum(str, Enum):
    tcp = "tcp"
    udp = "udp"
    sctp = "sctp"


class Port(OntolocyNode):

    __primarylabel__: ClassVar[str] = "Port"
    __primaryproperty__: ClassVar[str] = "unique_id"

    port_number: int
    protocol: PortProtocolEnum

    unique_id: Optional[UUID] = None

    @validator("unique_id", always=True)
    def generate_socket_uuid(cls, v: Optional[UUID], values: Dict[str, Any]) -> UUID:

        if v is None:

            key_values = [
                values["port_number"],
                values["protocol"],
            ]

            v = generate_deterministic_uuid(key_values)

        return v
