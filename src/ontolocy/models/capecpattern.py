from typing import ClassVar, Optional

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .cwe import CWE
from .mitreattacktechnique import MitreAttackTechnique


class CAPECPattern(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "capec_id"
    __primarylabel__: ClassVar[Optional[str]] = "CAPECPattern"

    capec_id: int
    description: Optional[str] = None
    name: str
    likelihood_of_attack: Optional[str] = None
    typical_severity: Optional[str] = None


#
# OUTGOING RELATIONSHIPS
#


class CAPECPatternMapsToAttackTechnique(OntolocyRelationship):
    source: CAPECPattern
    target: MitreAttackTechnique

    __relationshiptype__: ClassVar[str] = "CAPEC_PATTERN_MAPS_TO_ATTACK_TECHNIQUE"


class CAPECPatternRelatesToCWE(OntolocyRelationship):
    source: CAPECPattern
    target: CWE

    __relationshiptype__: ClassVar[str] = "CAPEC_PATTERN_RELATES_TO_CWE"
