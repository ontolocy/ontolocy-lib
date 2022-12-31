from typing import ClassVar, Optional

from pydantic import HttpUrl

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .actortype import ActorType
from .country import Country
from .mitreattacksoftware import MitreAttackSoftware
from .mitreattacktechnique import MitreAttackTechnique
from .threatactor import ThreatActor


class IntrusionSet(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "IntrusionSet"

    name: str
    unique_id: str
    name_giver: Optional[str]
    description: Optional[str]
    url_reference: Optional[HttpUrl]


#
# OUTGOING RELATIONSHIPS
#


class IntrusionSetAttributedToNation(OntolocyRelationship):
    source: IntrusionSet
    target: Country
    url_reference: Optional[HttpUrl]

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_ATTRIBUTED_TO_NATION"


class IntrusionSetLinkedToIntrusionSet(OntolocyRelationship):
    source: IntrusionSet
    target: IntrusionSet
    url_reference: Optional[HttpUrl]

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_LINKED_TO_INTRUSION_SET"


class IntrusionSetLinkedToThreatActor(OntolocyRelationship):
    source: IntrusionSet
    target: ThreatActor
    url_reference: Optional[HttpUrl]

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_LINKED_TO_THREAT_ACTOR"


class IntrusionSetIsOfType(OntolocyRelationship):
    source: IntrusionSet
    target: ActorType
    url_reference: Optional[HttpUrl]

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_IS_OF_TYPE"


class IntrusionSetUsesTechnique(OntolocyRelationship):
    source: IntrusionSet
    target: MitreAttackTechnique

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_USES_TECHNIQUE"


class IntrusionSetUsesSoftware(OntolocyRelationship):
    source: IntrusionSet
    target: MitreAttackSoftware

    __relationshiptype__: ClassVar[str] = "INTRUSION_SET_USES_SOFTWARE"
