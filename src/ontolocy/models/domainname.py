import re
from datetime import datetime
from typing import ClassVar, Optional

from pydantic import field_validator

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship


class DomainName(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "name"
    __primarylabel__: ClassVar[Optional[str]] = "DomainName"

    name: str

    @field_validator("name")
    @classmethod
    def validate_domain(cls, v: str) -> str:
        pattern = r"((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}"
        m = re.match(pattern, v)

        if m is None:
            raise ValueError("Doesn't look like a valid domain")

        return v


class DomainNameHasDNSRecord(OntolocyRelationship):
    __relationshiptype__: ClassVar[str] = "DOMAIN_NAME_HAS_DNS_RECORD"

    source: DomainName
    target: "DNSRecord"

    observation_date: datetime


from .dnsrecord import DNSRecord  # noqa: E402

DomainNameHasDNSRecord.model_rebuild()
