from typing import ClassVar, Optional

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .cve import CVE


class Organisation(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "name"
    __primarylabel__: ClassVar[str] = "Organisation"

    name: str
    address: Optional[str]


#
# OUTGOING RELATIONSHIPS
#


class OrganisationAssignedAssignedCVSSToCVE(OntolocyRelationship):
    source: Organisation
    target: CVE

    version: str
    vector_string: str
    attack_vector: str
    attack_complexity: str
    privileges_required: str
    user_interaction: str
    scope: str
    confidentiality_impact: str
    integrity_impact: str
    availability_impact: str
    base_score: float
    base_severity: str
    exploitability_score: float
    impact_score: float

    __relationshiptype__: ClassVar[str] = "ORGANISATION_ASSIGNED_CVSS_TO_CVE"
