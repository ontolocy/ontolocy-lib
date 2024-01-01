from datetime import date
from typing import ClassVar, Optional

from pydantic import AnyHttpUrl

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship

# from .cve import CVE

# from .report import Report


class Organisation(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "name"
    __primarylabel__: ClassVar[str] = "Organisation"

    name: str
    description: Optional[str] = None
    address: Optional[str] = None


#
# OUTGOING RELATIONSHIPS
#


class OrganisationAssignedCVSSToCVE(OntolocyRelationship):
    source: Organisation
    target: "CVE"

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


class OrganisationReportedExploitationOfCVE(OntolocyRelationship):
    source: Organisation
    target: "CVE"

    reported_date: date
    url_reference: Optional[AnyHttpUrl]
    description: Optional[str]
    required_action: Optional[str]

    __relationshiptype__: ClassVar[str] = "ORGANISATION_REPORTED_EXPLOITATION_OF_CVE"


class OrganisationPublishedThreatReport(OntolocyRelationship):
    __relationshiptype__: ClassVar[str] = "ORGANISATION_PUBLISHED_THREAT_REPORT"

    source: Organisation
    target: "Report"

    context: Optional[str]
    url_reference: Optional[AnyHttpUrl]


from .cve import CVE  # noqa: E402
from .report import Report  # noqa: E402

OrganisationAssignedCVSSToCVE.model_rebuild()
OrganisationPublishedThreatReport.model_rebuild()
OrganisationReportedExploitationOfCVE.model_rebuild()
