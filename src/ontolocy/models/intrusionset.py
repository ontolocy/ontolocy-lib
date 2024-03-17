from typing import ClassVar, List, Optional

from pydantic import HttpUrl

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


#
# OUTGOING RELATIONSHIPS
#


class IntrusionSetLinkedToMitreAttackGroup(OntolocyRelationship):
    source: IntrusionSet
    target: MitreAttackGroup

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_LINKED_TO_MITRE_ATTACK_GROUP"


class IntrusionSetAttributedToNation(OntolocyRelationship):
    source: IntrusionSet
    target: Country
    url_reference: Optional[HttpUrl] = None

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_ATTRIBUTED_TO_NATION"


class IntrusionSetLinkedToIntrusionSet(OntolocyRelationship):
    source: IntrusionSet
    target: IntrusionSet
    url_reference: Optional[HttpUrl] = None

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_LINKED_TO_INTRUSION_SET"


class IntrusionSetLinkedToThreatActor(OntolocyRelationship):
    source: IntrusionSet
    target: ThreatActor
    url_reference: Optional[HttpUrl] = None

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_LINKED_TO_THREAT_ACTOR"


class IntrusionSetIsOfType(OntolocyRelationship):
    source: IntrusionSet
    target: ActorType
    url_reference: Optional[HttpUrl] = None

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_IS_OF_TYPE"


class IntrusionSetUsesTechnique(OntolocyRelationship):
    source: IntrusionSet
    target: MitreAttackTechnique

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_USES_TECHNIQUE"


class IntrusionSetUsesSoftware(OntolocyRelationship):
    source: IntrusionSet
    target: MitreAttackSoftware

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_USES_SOFTWARE"
