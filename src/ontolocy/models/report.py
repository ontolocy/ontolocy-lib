from datetime import date
from typing import ClassVar, List, Optional

from pydantic import HttpUrl, ValidationInfo, field_validator

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from ..utils import generate_deterministic_uuid
from .campaign import Campaign
from .country import Country
from .cve import CVE
from .cyberharm import CyberHarm
from .intrusionset import IntrusionSet
from .ip import IPAddressNode
from .mitreattacksoftware import MitreAttackSoftware
from .mitreattacktechnique import MitreAttackTechnique
from .sector import Sector
from .threatactor import ThreatActor


class Report(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "Report"

    title: str
    author: str
    url_reference: HttpUrl
    published_date: date
    summary: Optional[str] = None

    additional_urls: Optional[List[HttpUrl]] = None
    unique_id: Optional[str] = None

    def __str__(self) -> str:
        return self.title

    @field_validator("unique_id")
    def generate_socket_uuid(cls, v: Optional[str], info: ValidationInfo) -> str:
        values = info.data

        if v is None:
            key_values = [values["title"], values["author"], values["published_date"]]

            v = str(generate_deterministic_uuid(key_values))

        return v


#
# OUTGOING RELATIONSHIPS
#


class ReportMentionsIntrusionSet(OntolocyRelationship):
    source: Report
    target: IntrusionSet

    __relationshiptype__: ClassVar[str] = "REPORT_MENTIONS_INTRUSION_SET"


class ReportMentionsTechnique(OntolocyRelationship):
    source: Report
    target: MitreAttackTechnique

    __relationshiptype__: ClassVar[str] = "REPORT_MENTIONS_TECHNIQUE"


class ReportMentionsCVE(OntolocyRelationship):
    source: Report
    target: CVE

    __relationshiptype__: ClassVar[str] = "REPORT_MENTIONS_CVE"


class ReportMentionsSector(OntolocyRelationship):
    source: Report
    target: Sector

    __relationshiptype__: ClassVar[str] = "REPORT_MENTIONS_SECTOR"


class ReportMentionsCountry(OntolocyRelationship):
    source: Report
    target: Country

    __relationshiptype__: ClassVar[str] = "REPORT_MENTIONS_COUNTRY"


class ReportMentionsIP(OntolocyRelationship):
    source: Report
    target: IPAddressNode

    __relationshiptype__: ClassVar[str] = "REPORT_MENTIONS_IP"


class ReportIdentifiesIntrusionSet(OntolocyRelationship):
    source: Report
    target: IntrusionSet

    __relationshiptype__: ClassVar[str] = "REPORT_IDENTIFIES_INTRUSION_SET"


class ReportIdentifiesThreatActor(OntolocyRelationship):
    source: Report
    target: ThreatActor

    __relationshiptype__: ClassVar[str] = "REPORT_IDENTIFIES_THREAT_ACTOR"


class ReportIdentifiesTechnique(OntolocyRelationship):
    source: Report
    target: MitreAttackTechnique

    __relationshiptype__: ClassVar[str] = "REPORT_IDENTIFIES_TECHNIQUE"


class ReportIdentifiesCVE(OntolocyRelationship):
    source: Report
    target: CVE

    __relationshiptype__: ClassVar[str] = "REPORT_IDENTIFIES_CVE"


class ReportIdentifiesVictimSector(OntolocyRelationship):
    source: Report
    target: Sector

    __relationshiptype__: ClassVar[str] = "REPORT_IDENTIFIES_VICTIM_SECTOR"


class ReportIdentifiesVictimCountry(OntolocyRelationship):
    source: Report
    target: Country

    __relationshiptype__: ClassVar[str] = "REPORT_IDENTIFIES_VICTIM_COUNTRY"


class ReportIdentifiesSponsorCountry(OntolocyRelationship):
    source: Report
    target: Country

    __relationshiptype__: ClassVar[str] = "REPORT_IDENTIFIES_SPONSOR_COUNTRY"


class ReportIdentifiesCyberHarm(OntolocyRelationship):
    source: Report
    target: CyberHarm

    __relationshiptype__: ClassVar[str] = "REPORT_IDENTIFIES_CYBER_HARM"


class ReportIdentifiesCampaign(OntolocyRelationship):
    source: Report
    target: Campaign

    __relationshiptype__: ClassVar[str] = "REPORT_IDENTIFIES_CAMPAIGN"


class ReportIdentifiesSoftware(OntolocyRelationship):
    source: Report
    target: MitreAttackSoftware

    __relationshiptype__: ClassVar[str] = "REPORT_IDENTIFIES_SOFTWARE"
