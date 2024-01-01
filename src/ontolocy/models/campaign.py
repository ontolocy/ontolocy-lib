from datetime import datetime
from typing import ClassVar, Optional

from pydantic import HttpUrl

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .country import Country
from .cve import CVE
from .cyberharm import CyberHarm
from .intrusionset import IntrusionSet
from .mitreattacktechnique import MitreAttackTechnique
from .sector import Sector


class Campaign(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "Campaign"

    title: str
    url_reference: HttpUrl
    activity_datetime: datetime
    summary: Optional[str]
    unique_id: str

    def __str__(self) -> str:
        return self.title


#
# OUTGOING RELATIONSHIPS
#


class CampaignByIntrusionSet(OntolocyRelationship):
    source: Campaign
    target: IntrusionSet
    url_reference: Optional[HttpUrl]

    __relationshiptype__: ClassVar[str] = "CAMPAIGN_BY_INTRUSION_SET"


class CampaignUsesTechnique(OntolocyRelationship):
    source: Campaign
    target: MitreAttackTechnique
    url_reference: Optional[HttpUrl]

    __relationshiptype__: ClassVar[str] = "CAMPAIGN_USES_TECHNIQUE"


class CampaignUsesCVE(OntolocyRelationship):
    source: Campaign
    target: CVE
    url_reference: Optional[HttpUrl]

    __relationshiptype__: ClassVar[str] = "CAMPAIGN_USES_CVE"


class CampaignTargetsSector(OntolocyRelationship):
    source: Campaign
    target: Sector
    url_reference: Optional[HttpUrl]

    __relationshiptype__: ClassVar[str] = "CAMPAIGN_TARGETS_SECTOR"


class CampaignTargetsCountry(OntolocyRelationship):
    source: Campaign
    target: Country
    url_reference: Optional[HttpUrl]

    __relationshiptype__: ClassVar[str] = "CAMPAIGN_TARGETS_COUNTRY"


class CampaignCausedCyberHarm(OntolocyRelationship):
    source: Campaign
    target: CyberHarm
    url_reference: Optional[HttpUrl]

    __relationshiptype__: ClassVar[str] = "CAMPAIGN_CAUSED_CYBER_HARM"
