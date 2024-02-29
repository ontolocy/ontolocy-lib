from typing import ClassVar, List, Optional

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
    additional_urls: Optional[List[HttpUrl]] = None

    def __str__(self):
        return self.name


#
# OUTGOING RELATIONSHIPS
#


class ThreatActorAttributedToNation(OntolocyRelationship):
    source: ThreatActor
    target: Country
    url_reference: Optional[HttpUrl] = None

    __relationshiptype__: ClassVar[str] = "THREAT_ACTOR_ATTRIBUTED_TO_NATION"


class ThreatActorIsOfType(OntolocyRelationship):
    source: ThreatActor
    target: ActorType
    url_reference: Optional[HttpUrl] = None

    __relationshiptype__: ClassVar[str] = "THREAT_ACTOR_IS_OF_TYPE"


class ThreatActorLinkedToThreatActor(OntolocyRelationship):
    source: ThreatActor
    target: ThreatActor
    url_reference: Optional[HttpUrl] = None
    context: Optional[str] = None

    __relationshiptype__: ClassVar[str] = "THREAT_ACTOR_LINKED_TO_THREAT_ACTOR"
