from typing import ClassVar, Optional

from pydantic import IPvAnyNetwork

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .organisation import Organisation


class ASN(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "number"
    __primarylabel__: ClassVar[Optional[str]] = "ASN"

    number: int
    network_name: str
    description: str
    cidr: IPvAnyNetwork
    country_code: str
    registry: str


#
# OUTGOING RELATIONSHIPS
#


class ASNHasWhoIsRegisteredContact(OntolocyRelationship):

    __relationshiptype__: ClassVar[str] = "ASN_HAS_REGISTERED_CONTACT"

    source: ASN
    target: Organisation
