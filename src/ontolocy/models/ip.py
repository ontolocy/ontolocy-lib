from enum import Enum
from ipaddress import ip_address
from typing import ClassVar, Optional
from uuid import UUID, uuid4

from pydantic import IPvAnyAddress, ValidationInfo, field_validator

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from ..utils import generate_deterministic_uuid
from .asn import ASN
from .country import Country
from .cpe import CPE
from .listeningsocket import ListeningSocket
from .macaddress import MACAddress


class IPVersionEnum(str, Enum):
    ipv4 = "ipv4"
    ipv6 = "ipv6"


class IPAddressNode(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[str] = "IPAddress"

    ip_address: IPvAnyAddress
    ip_version: Optional[IPVersionEnum] = None
    private: Optional[bool] = None
    namespace: Optional[str] = None

    unique_id: Optional[str] = None

    def __str__(self) -> str:
        return str(self.ip_address)

    @field_validator("ip_address", mode="before")
    @classmethod
    def refang_ip(cls, v: str):
        """Some reports will 'de-fang' an IP with square brackets.
        Remove them for consistency"""
        return v.replace("[", "").replace("]", "")

    @field_validator("ip_version")
    def mark_ip_version(cls, v, info: ValidationInfo):
        values = info.data
        versions = {4: IPVersionEnum.ipv4, 6: IPVersionEnum.ipv6}
        if v is None and "ip_address" in values:
            return versions[ip_address(values["ip_address"]).version]
        else:
            return v

    @field_validator("private")
    def mark_private(cls, v, info: ValidationInfo):
        values = info.data
        if v is None and "ip_address" in values:
            return ip_address(values["ip_address"]).is_private
        else:
            return v

    @field_validator("namespace")
    def set_namespace(cls, v, info: ValidationInfo):
        values = info.data
        if values["private"] is False:
            return None

        elif v is None:
            return str(uuid4())

        else:
            return v

    @field_validator("unique_id")
    def generate_instance_id(cls, v: Optional[UUID], info: ValidationInfo) -> str:
        values = info.data
        if v is None and values["private"] and values.get("namespace"):
            key_values = [values["ip_address"], values["namespace"]]

            v = str(generate_deterministic_uuid(key_values))

        elif v is None:
            v = str(values["ip_address"])

        return v


class IPAddressHasOpenPort(OntolocyRelationship):
    __relationshiptype__: ClassVar[str] = "IP_ADDRESS_HAS_OPEN_PORT"

    source: IPAddressNode
    target: ListeningSocket


class IPAddressBelongsToASN(OntolocyRelationship):
    __relationshiptype__: ClassVar[str] = "IP_ADDRESS_BELONGS_TO_ASN"

    source: IPAddressNode
    target: ASN


class IPAddressLocatedInCountry(OntolocyRelationship):
    __relationshiptype__: ClassVar[str] = "IP_ADDRESS_LOCATED_IN_COUNTRY"

    source: IPAddressNode
    target: Country


class IPAddressIdentifiedAsPlatform(OntolocyRelationship):
    __relationshiptype__: ClassVar[str] = "IP_ADDRESS_IDENTIFIED_AS_PLATFORM"

    source: IPAddressNode
    target: CPE


class IPAddressMapsToMACAddress(OntolocyRelationship):
    __relationshiptype__: ClassVar[str] = "IP_ADDRESS_MAPS_TO_MAC_ADDRESS"

    source: IPAddressNode
    target: MACAddress


class IPAddressObservedWithHostname(OntolocyRelationship):
    __relationshiptype__: ClassVar[str] = "IP_ADDRESS_OBSERVED_WITH_HOSTNAME"

    source: IPAddressNode
    target: "DomainName"


from .domainname import DomainName  # noqa: E402

IPAddressObservedWithHostname.model_rebuild()
