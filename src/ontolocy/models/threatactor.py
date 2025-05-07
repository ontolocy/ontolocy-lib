from typing import ClassVar, List, Optional

from pydantic import HttpUrl, field_serializer

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .actortype import ActorType
from .country import Country


class ThreatActor(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "ThreatActor"

    name: str
    unique_id: str
    description: Optional[str] = None
    url_reference: Optional[HttpUrl] = None
    additional_urls: Optional[List[HttpUrl]] = None

    def __str__(self):
        return self.name

    @field_serializer("url_reference")
    def serialize_to_str(self, input: Optional[HttpUrl], _info):
        if input:
            return str(input)

    @field_serializer("additional_urls")
    def serialize_list_to_str(self, input: Optional[List[HttpUrl]], _info):
        if input:
            return [str(url) for url in input]


#
# OUTGOING RELATIONSHIPS
#


class ThreatActorAttributedToNation(OntolocyRelationship):
    source: ThreatActor
    target: Country
    url_reference: Optional[HttpUrl] = None

    __relationshiptype__: ClassVar[str] = "THREAT_ACTOR_ATTRIBUTED_TO_NATION"

    @field_serializer("url_reference")
    def serialize_to_str(self, input: Optional[HttpUrl], _info):
        if input:
            return str(input)


class ThreatActorIsOfType(OntolocyRelationship):
    source: ThreatActor
    target: ActorType
    url_reference: Optional[HttpUrl] = None

    __relationshiptype__: ClassVar[str] = "THREAT_ACTOR_IS_OF_TYPE"

    @field_serializer("url_reference")
    def serialize_to_str(self, input: Optional[HttpUrl], _info):
        if input:
            return str(input)


class ThreatActorLinkedToThreatActor(OntolocyRelationship):
    source: ThreatActor
    target: ThreatActor
    url_reference: Optional[HttpUrl] = None
    context: Optional[str] = None

    __relationshiptype__: ClassVar[str] = "THREAT_ACTOR_LINKED_TO_THREAT_ACTOR"

    @field_serializer("url_reference")
    def serialize_to_str(self, input: Optional[HttpUrl], _info):
        if input:
            return str(input)
