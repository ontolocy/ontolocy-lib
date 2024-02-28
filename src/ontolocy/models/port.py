from enum import Enum
from typing import ClassVar, Optional

from pydantic import ValidationInfo, field_validator

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

    unique_id: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.port_number} ({self.protocol.value})"

    @field_validator("unique_id")
    def generate_socket_uuid(cls, v: Optional[str], info: ValidationInfo) -> str:
        values = info.data

        if v is None:
            key_values = [
                values["port_number"],
                values["protocol"],
            ]

            v = str(generate_deterministic_uuid(key_values))

        return v
