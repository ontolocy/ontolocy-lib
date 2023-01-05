from ontolocy.dataorigin import DataOrigin
from ontolocy.models.actortype import ActorType
from ontolocy.models.asn import ASN, ASNHasWhoIsRegisteredContact
from ontolocy.models.banner import Banner
from ontolocy.models.campaign import (
    Campaign,
    CampaignByIntrusionSet,
    CampaignCausedCyberHarm,
    CampaignTargetsCountry,
    CampaignTargetsSector,
    CampaignUsesCVE,
    CampaignUsesTechnique,
)
from ontolocy.models.capecpattern import (
    CAPECPattern,
    CAPECPatternMapsToAttackTechnique,
    CAPECPatternRelatesToCWE,
)
from ontolocy.models.cobaltstrikebeacon import (
    CobaltStikeBeaconCollectedFrom,
    CobaltStikeBeaconHasWatermark,
    CobaltStrikeBeacon,
)
from ontolocy.models.cobaltstrikewatermark import CobaltStrikeWatermark
from ontolocy.models.country import Country
from ontolocy.models.cpe import CPE
from ontolocy.models.cve import CVE, CVERelatesToCPE, CVERelatesToCWE
from ontolocy.models.cwe import CWE
from ontolocy.models.cyberharm import CyberHarm
from ontolocy.models.exploit import Exploit, ExploitExploitsVulnerability
from ontolocy.models.intrusionset import (
    IntrusionSet,
    IntrusionSetAttributedToNation,
    IntrusionSetIsOfType,
    IntrusionSetLinkedToIntrusionSet,
    IntrusionSetLinkedToThreatActor,
    IntrusionSetUsesSoftware,
    IntrusionSetUsesTechnique,
)
from ontolocy.models.ip import (
    IPAddressBelongsToASN,
    IPAddressHasOpenPort,
    IPAddressLocatedInCountry,
    IPAddressNode,
)
from ontolocy.models.jarmhash import JarmHash
from ontolocy.models.listeningsocket import (
    ListeningSocket,
    ListeningSocketUsesPort,
    OpenPortHasJarmHash,
    OpenPortPresentsBanner,
    OpenPortPresentsX509Certificate,
    ServiceHostsURL,
    ServiceIdentifiedAsPlatform,
)
from ontolocy.models.mitreattackcampaign import (
    MitreAttackCampaign,
    MitreCampaignAttributedTo,
    MitreCampaignUsesSoftware,
    MitreCampaignUsesTechnique,
)
from ontolocy.models.mitreattacksoftware import (
    MitreAttackSoftware,
    MitreSoftwareUsesTechnique,
)
from ontolocy.models.mitreattacktactic import (
    MitreAttackTactic,
    MitreTacticIncludesTechnique,
)
from ontolocy.models.mitreattacktechnique import (
    MitreAttackTechnique,
    MitreSubtechniqueOf,
)
from ontolocy.models.networkservice import NetworkService, NetworkServiceRunsOnPort
from ontolocy.models.organisation import (
    Organisation,
    OrganisationAssignedAssignedCVSSToCVE,
)
from ontolocy.models.port import Port
from ontolocy.models.report import (
    Report,
    ReportIdentifiesCampaign,
    ReportIdentifiesCVE,
    ReportIdentifiesCyberHarm,
    ReportIdentifiesIntrusionSet,
    ReportIdentifiesSoftware,
    ReportIdentifiesSponsorCountry,
    ReportIdentifiesTechnique,
    ReportIdentifiesVictimCountry,
    ReportIdentifiesVictimSector,
    ReportMentionsCountry,
    ReportMentionsCVE,
    ReportMentionsIntrusionSet,
    ReportMentionsIP,
    ReportMentionsSector,
    ReportMentionsTechnique,
)
from ontolocy.models.sector import Sector
from ontolocy.models.threatactor import (
    ThreatActor,
    ThreatActorAttributedToNation,
    ThreatActorIsOfType,
)
from ontolocy.models.url import URLNode, UrlRedirectsToUrl
from ontolocy.models.x509certificate import X509Certificate
from ontolocy.utils import init_ontolocy

__all__ = [
    "DataOrigin",
    "init_ontolocy",
    # models
    "ActorType",
    "ASN",
    "ASNHasWhoIsRegisteredContact",
    "Banner",
    "Campaign",
    "CampaignByIntrusionSet",
    "CampaignUsesTechnique",
    "CampaignUsesCVE",
    "CampaignTargetsSector",
    "CampaignTargetsCountry",
    "CampaignCausedCyberHarm",
    "CAPECPattern",
    "CAPECPatternMapsToAttackTechnique",
    "CAPECPatternRelatesToCWE",
    "CobaltStrikeBeacon",
    "CobaltStikeBeaconCollectedFrom",
    "CobaltStikeBeaconHasWatermark",
    "CobaltStrikeWatermark",
    "Country",
    "CPE",
    "CVE",
    "CVERelatesToCPE",
    "CVERelatesToCWE",
    "CWE",
    "CyberHarm",
    "Exploit",
    "ExploitExploitsVulnerability",
    "IntrusionSet",
    "IntrusionSetAttributedToNation",
    "IntrusionSetLinkedToIntrusionSet",
    "IntrusionSetIsOfType",
    "IntrusionSetLinkedToThreatActor",
    "IntrusionSetUsesSoftware",
    "IntrusionSetUsesTechnique",
    "IPAddressNode",
    "IPAddressBelongsToASN",
    "IPAddressHasOpenPort",
    "IPAddressLocatedInCountry",
    "JarmHash",
    "ListeningSocket",
    "ListeningSocketUsesPort",
    "ServiceIdentifiedAsPlatform",
    "MitreAttackTactic",
    "MitreTacticIncludesTechnique",
    "MitreAttackTechnique",
    "MitreSubtechniqueOf",
    "MitreAttackCampaign",
    "MitreCampaignUsesSoftware",
    "MitreCampaignUsesTechnique",
    "MitreAttackSoftware",
    "MitreSoftwareUsesTechnique",
    "MitreCampaignAttributedTo",
    "NetworkService",
    "NetworkServiceRunsOnPort",
    "OpenPortHasJarmHash",
    "OpenPortPresentsBanner",
    "OpenPortPresentsX509Certificate",
    "Organisation",
    "OrganisationAssignedAssignedCVSSToCVE",
    "Port",
    "Report",
    "ReportMentionsCountry",
    "ReportMentionsCVE",
    "ReportMentionsIntrusionSet",
    "ReportMentionsIP",
    "ReportMentionsSector",
    "ReportMentionsTechnique",
    "ReportIdentifiesIntrusionSet",
    "ReportIdentifiesTechnique",
    "ReportIdentifiesCVE",
    "ReportIdentifiesVictimSector",
    "ReportIdentifiesVictimCountry",
    "ReportIdentifiesSponsorCountry",
    "ReportIdentifiesCyberHarm",
    "ReportIdentifiesCampaign",
    "ReportIdentifiesSoftware",
    "Sector",
    "ServiceHostsURL",
    "ThreatActor",
    "ThreatActorAttributedToNation",
    "ThreatActorIsOfType",
    "X509Certificate",
    "URLNode",
    "UrlRedirectsToUrl",
]
