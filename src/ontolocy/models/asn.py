from typing import ClassVar, Optional

from pydantic import IPvAnyNetwork, field_serializer

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship


class ASN(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "number"
    __primarylabel__: ClassVar[Optional[str]] = "ASN"

    number: int
    network_name: str
    description: str
    cidr: IPvAnyNetwork
    country_code: str
    registry: str

    @field_serializer("cidr")
    def serialize_cidr(self, input: IPvAnyNetwork, _info):
        return str(input)


#
# OUTGOING RELATIONSHIPS
#


class ASNHasWhoIsRegisteredContact(OntolocyRelationship):
    __relationshiptype__: ClassVar[str] = "ASN_HAS_REGISTERED_CONTACT"

    source: ASN
    target: "Organisation"


from .organisation import Organisation  # noqa: E402

ASNHasWhoIsRegisteredContact.model_rebuild()
