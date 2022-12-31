from typing import Any, ClassVar, Dict, Optional
from uuid import UUID

from pydantic import validator

from ..node import OntolocyNode
from ..utils import generate_deterministic_uuid


class DNSRecord(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "DNSRecord"

    type: str
    name: str
    content: str

    unique_id: Optional[UUID]

    @validator("unique_id", always=True)
    def generate_dnsrecord_uuid(cls, v: Optional[UUID], values: Dict[str, Any]) -> UUID:

        if v is None:

            key_values = [
                values["type"],
                values["name"],
                values["content"],
            ]

            v = generate_deterministic_uuid(key_values)

        return v
