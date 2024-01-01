from datetime import datetime
from typing import ClassVar, Optional
from uuid import UUID

from pydantic import ValidationInfo, field_validator

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from ..utils import generate_deterministic_uuid


class DNSRecord(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "DNSRecord"

    type: str
    name: str
    content: str

    unique_id: Optional[UUID] = None

    @field_validator("unique_id")
    def generate_dnsrecord_uuid(cls, v: Optional[UUID], info: ValidationInfo) -> UUID:
        values = info.data

        if v is None:
            key_values = [
                values["type"],
                values["name"],
                values["content"],
            ]

            v = generate_deterministic_uuid(key_values)

        return v


class DNSRecordPointsToIPAddress(OntolocyRelationship):
    __relationshiptype__: ClassVar[str] = "DNS_RECORD_POINTS_TO_IP_ADDRESS"

    source: DNSRecord
    target: "IPAddressNode"

    observation_date: datetime


class DNSRecordPointsToDomainName(OntolocyRelationship):
    __relationshiptype__: ClassVar[str] = "DNS_RECORD_POINTS_TO_DOMAIN_NAME"

    source: DNSRecord
    target: "DomainName"

    observation_date: datetime


class DNSRecordForDomain(OntolocyRelationship):
    __relationshiptype__: ClassVar[str] = "DNS_RECORD_FOR_DOMAIN"

    source: DNSRecord
    target: "DomainName"

    observation_date: datetime


from .domainname import DomainName  # noqa: E402

DNSRecordPointsToDomainName.model_rebuild()
DNSRecordForDomain.model_rebuild()

from .ip import IPAddressNode  # noqa: E402

DNSRecordPointsToIPAddress.model_rebuild()
