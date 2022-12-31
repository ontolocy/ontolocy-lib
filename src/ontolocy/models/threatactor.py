from typing import ClassVar, Optional

from pydantic import HttpUrl

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .actortype import ActorType
from .country import Country


class ThreatActor(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "ThreatActor"

    name: str
    unique_id: str
    description: Optional[str]
    url_reference: Optional[HttpUrl]


#
# OUTGOING RELATIONSHIPS
#


class ThreatActorAttributedToNation(OntolocyRelationship):
    source: ThreatActor
    target: Country
    url_reference: Optional[HttpUrl]

    __relationshiptype__: ClassVar[str] = "THREAT_ACTOR_ATTRIBUTED_TO_NATION"


class ThreatActorIsOfType(OntolocyRelationship):
    source: ThreatActor
    target: ActorType
    url_reference: Optional[HttpUrl]

    __relationshiptype__: ClassVar[str] = "THREAT_ACTOR_IS_OF_TYPE"
