from datetime import datetime
from typing import ClassVar, Optional

from pydantic import Field, ValidationInfo, field_validator

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from ..utils import generate_deterministic_uuid


class DNSRecord(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "DNSRecord"

    type: str
    name: str
    content: str
    record_class: str = "IN"

    ttl: Optional[int] = None

    unique_id: Optional[str] = None

    @field_validator("unique_id")
    def generate_dnsrecord_uuid(cls, v: Optional[str], info: ValidationInfo) -> str:
        values = info.data

        if v is None:
            key_values = [
                values["type"],
                values["name"],
                values["content"],
            ]

            v = generate_deterministic_uuid(key_values)

        return str(v)


class DNSRecordPointsToIPAddress(OntolocyRelationship):
    __relationshiptype__: ClassVar[str] = "DNS_RECORD_POINTS_TO_IP_ADDRESS"

    source: DNSRecord
    target: "IPAddressNode"

    observation_date: datetime = Field(default_factory=datetime.now)


class DNSRecordPointsToDomainName(OntolocyRelationship):
    __relationshiptype__: ClassVar[str] = "DNS_RECORD_POINTS_TO_DOMAIN_NAME"

    source: DNSRecord
    target: "DomainName"

    observation_date: datetime = Field(default_factory=datetime.now)


from .domainname import DomainName  # noqa: E402

DNSRecordPointsToDomainName.model_rebuild()


from .ip import IPAddressNode  # noqa: E402

DNSRecordPointsToIPAddress.model_rebuild()
