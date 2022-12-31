from enum import Enum
from ipaddress import ip_address
from typing import Any, ClassVar, Dict, Optional
from uuid import UUID, uuid4

from pydantic import IPvAnyAddress, validator

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from ..utils import generate_deterministic_uuid
from .asn import ASN
from .country import Country
from .listeningsocket import ListeningSocket


class IPVersionEnum(str, Enum):
    ipv4 = "ipv4"
    ipv6 = "ipv6"


class IPAddressNode(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[str] = "IPAddress"

    ip_address: IPvAnyAddress
    ip_version: Optional[IPVersionEnum]
    private: Optional[bool] = None
    namespace: Optional[str] = None

    unique_id: Optional[UUID] = None

    @validator("ip_address", pre=True)
    def refang_ip(cls, v: str):
        """Some reports will 'de-fang' an IP with square brackets.
        Remove them for consistency"""
        return v.replace("[", "").replace("]", "")

    @validator("ip_version", always=True)
    def mark_ip_version(cls, v, values: Dict[str, Any]):

        versions = {4: IPVersionEnum.ipv4, 6: IPVersionEnum.ipv6}
        if v is None and "ip_address" in values:
            return versions[ip_address(values["ip_address"]).version]
        else:
            return v

    @validator("private", always=True)
    def mark_private(cls, v, values: Dict[str, Any]):
        if v is None and "ip_address" in values:
            return ip_address(values["ip_address"]).is_private
        else:
            return v

    @validator("namespace", always=True)
    def set_namespace(cls, v, values: Dict[str, Any]):
        if values["private"] is False:
            return None

        elif v is None:
            return str(uuid4())

        else:
            return v

    @validator("unique_id", always=True)
    def generate_instance_id(cls, v: Optional[UUID], values: Dict[str, Any]) -> UUID:

        if v is None:

            key_values = [values["ip_address"], values["namespace"]]

            v = generate_deterministic_uuid(key_values)

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
