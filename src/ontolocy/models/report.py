from datetime import date
from typing import ClassVar, Optional

from pydantic import HttpUrl

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .campaign import Campaign
from .country import Country
from .cve import CVE
from .cyberharm import CyberHarm
from .intrusionset import IntrusionSet
from .ip import IPAddressNode
from .mitreattacksoftware import MitreAttackSoftware
from .mitreattacktechnique import MitreAttackTechnique
from .sector import Sector


class Report(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "url_reference"
    __primarylabel__: ClassVar[Optional[str]] = "Report"

    title: str
    author: str
    url_reference: HttpUrl
    published_date: date
    summary: Optional[str]


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
