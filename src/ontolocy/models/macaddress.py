from typing import ClassVar, Optional

from pydantic import StringConstraints, field_validator
from typing_extensions import Annotated

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .host import Host


class MACAddress(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "mac_address"
    __primarylabel__: ClassVar[Optional[str]] = "MACAddress"

    mac_address: Annotated[
        str,
        StringConstraints(
            pattern=r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"  # noqa: F722
        ),
    ]

    @field_validator("mac_address")
    def format_mac_address(cls, v: str) -> str:
        """We want to standardize on colons and uppercase letters"""

        v = v.upper()
        v = v.replace("-", ":")

        return v


class MACAddressAssignedToHost(OntolocyRelationship):
    __relationshiptype__: ClassVar[str] = "MAC_ADDRESS_ASSIGNED_TO_HOST"

    source: MACAddress
    target: Host

    interface: Optional[str] = None
