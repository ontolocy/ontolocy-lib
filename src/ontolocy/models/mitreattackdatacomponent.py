from datetime import datetime
from typing import ClassVar, Optional

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .mitreattacktechnique import MitreAttackTechnique


class MitreAttackDataComponent(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "stix_id"
    __primarylabel__: ClassVar[str] = "MitreAttackDataComponent"

    stix_id: str
    stix_type: str
    stix_created: datetime
    stix_modified: datetime
    stix_spec_version: str = "2.1"
    stix_revoked: Optional[bool] = False

    attack_spec_version: str
    attack_version: str
    attack_deprecated: Optional[bool] = False

    name: str
    description: str


#
# OUTGOING RELATIONSHIPS
#


class MitreAttackDataComponentDetectsTechnique(OntolocyRelationship):
    source: MitreAttackDataComponent
    target: MitreAttackTechnique

    __relationshiptype__: ClassVar[
        str
    ] = "MITRE_ATTACK_DATA_COMPONENT_DETECTS_TECHNIQUE"
