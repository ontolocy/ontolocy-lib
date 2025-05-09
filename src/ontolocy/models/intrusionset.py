from typing import ClassVar, List, Optional

from neontology import related_property
from pydantic import HttpUrl, field_serializer

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .actortype import ActorType
from .country import Country
from .mitreattackgroup import MitreAttackGroup
from .mitreattacksoftware import MitreAttackSoftware
from .mitreattacktechnique import MitreAttackTechnique
from .threatactor import ThreatActor


class IntrusionSet(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "IntrusionSet"

    name: str
    unique_id: str
    description: Optional[str] = None
    url_reference: Optional[HttpUrl] = None
    additional_urls: Optional[List[HttpUrl]] = None

    def __str__(self):
        return self.name

    @property
    @related_property
    def actor_types(self):
        return "MATCH (#ThisNode)-[:INTRUSION_SET_IS_OF_TYPE]->(at) RETURN COLLECT(at.name)"

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


class IntrusionSetLinkedToMitreAttackGroup(OntolocyRelationship):
    source: IntrusionSet
    target: MitreAttackGroup
    url_reference: Optional[HttpUrl] = None

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_LINKED_TO_MITRE_ATTACK_GROUP"

    @field_serializer("url_reference")
    def serialize_to_str(self, input: Optional[HttpUrl], _info):
        if input:
            return str(input)


class IntrusionSetAttributedToNation(OntolocyRelationship):
    source: IntrusionSet
    target: Country
    url_reference: Optional[HttpUrl] = None

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_ATTRIBUTED_TO_NATION"

    @field_serializer("url_reference")
    def serialize_to_str(self, input: Optional[HttpUrl], _info):
        if input:
            return str(input)


class IntrusionSetLinkedToIntrusionSet(OntolocyRelationship):
    source: IntrusionSet
    target: IntrusionSet
    url_reference: Optional[HttpUrl] = None

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_LINKED_TO_INTRUSION_SET"

    @field_serializer("url_reference")
    def serialize_to_str(self, input: Optional[HttpUrl], _info):
        if input:
            return str(input)


class IntrusionSetAffiliatedWithIntrusionSet(OntolocyRelationship):
    source: IntrusionSet
    target: IntrusionSet
    url_reference: Optional[HttpUrl] = None
    context: Optional[str] = None

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_AFFILIATED_WITH_INTRUSION_SET"

    @field_serializer("url_reference")
    def serialize_to_str(self, input: Optional[HttpUrl], _info):
        if input:
            return str(input)


class IntrusionSetLinkedToThreatActor(OntolocyRelationship):
    source: IntrusionSet
    target: ThreatActor
    url_reference: Optional[HttpUrl] = None

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_LINKED_TO_THREAT_ACTOR"

    @field_serializer("url_reference")
    def serialize_to_str(self, input: Optional[HttpUrl], _info):
        if input:
            return str(input)


class IntrusionSetIsOfType(OntolocyRelationship):
    source: IntrusionSet
    target: ActorType
    url_reference: Optional[HttpUrl] = None

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_IS_OF_TYPE"

    @field_serializer("url_reference")
    def serialize_to_str(self, input: Optional[HttpUrl], _info):
        if input:
            return str(input)


class IntrusionSetUsesTechnique(OntolocyRelationship):
    source: IntrusionSet
    target: MitreAttackTechnique

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_USES_TECHNIQUE"


class IntrusionSetUsesSoftware(OntolocyRelationship):
    source: IntrusionSet
    target: MitreAttackSoftware

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_USES_SOFTWARE"
