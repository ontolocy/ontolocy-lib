from ontolocy.dataorigin import DataOrigin, OriginGenerated
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
from ontolocy.models.control import (
    Control,
    ControlHasParentControl,
    ControlMitigatesAttackTechnique,
    ControlRelatedToControl,
)
from ontolocy.models.country import Country
from ontolocy.models.cpe import CPE
from ontolocy.models.cve import CVE, CVERelatesToCPE, CVERelatesToCWE
from ontolocy.models.cwe import CWE
from ontolocy.models.cyberharm import CyberHarm
from ontolocy.models.dnsrecord import (
    DNSRecord,
    DNSRecordForDomain,
    DNSRecordPointsToDomainName,
    DNSRecordPointsToIPAddress,
)
from ontolocy.models.domainname import DomainName, DomainNameHasDNSRecord
from ontolocy.models.exploit import Exploit, ExploitExploitsVulnerability
from ontolocy.models.host import Host
from ontolocy.models.intrusionset import (
    IntrusionSet,
    IntrusionSetAttributedToNation,
    IntrusionSetIsOfType,
    IntrusionSetLinkedToIntrusionSet,
    IntrusionSetLinkedToMitreAttackGroup,
    IntrusionSetLinkedToThreatActor,
    IntrusionSetUsesSoftware,
    IntrusionSetUsesTechnique,
)
from ontolocy.models.ip import (
    IPAddressBelongsToASN,
    IPAddressHasOpenPort,
    IPAddressIdentifiedAsPlatform,
    IPAddressLocatedInCountry,
    IPAddressMapsToMACAddress,
    IPAddressNode,
    IPAddressObservedWithHostname,
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
from ontolocy.models.macaddress import MACAddress, MACAddressAssignedToHost
from ontolocy.models.mitreattackcampaign import (
    MitreAttackCampaign,
    MitreCampaignAttributedTo,
    MitreCampaignUsesSoftware,
    MitreCampaignUsesTechnique,
)
from ontolocy.models.mitreattackdatacomponent import (
    MitreAttackDataComponent,
    MitreAttackDataComponentDetectsTechnique,
)
from ontolocy.models.mitreattackdatasource import (
    MitreAttackDataSource,
    MitreAttackDataSourceHasComponent,
)
from ontolocy.models.mitreattackgroup import (
    MitreAttackGroup,
    MitreAttackGroupUsesSoftware,
    MitreAttackGroupUsesTechnique,
)
from ontolocy.models.mitreattackmitigation import (
    MitreAttackMitigation,
    MitreAttackMitigationDefendsAgainstTechnique,
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
    OrganisationAssignedCVSSToCVE,
    OrganisationPublishedThreatReport,
    OrganisationReportedExploitationOfCVE,
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
from ontolocy.models.useraccount import UserAccount, UserAccountAuthorizedOnHost
from ontolocy.models.x509certificate import X509Certificate
from ontolocy.node import OntolocyNode
from ontolocy.relationship import OntolocyRelationship
from ontolocy.utils import init_ontolocy

__all__ = [
    "DataOrigin",
    "OriginGenerated",
    "OntolocyNode",
    "OntolocyRelationship",
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
    "Control",
    "ControlHasParentControl",
    "ControlMitigatesAttackTechnique",
    "ControlRelatedToControl",
    "Country",
    "CPE",
    "CVE",
    "CVERelatesToCPE",
    "CVERelatesToCWE",
    "CWE",
    "CyberHarm",
    "DNSRecord",
    "DNSRecordForDomain",
    "DNSRecordPointsToDomainName",
    "DNSRecordPointsToIPAddress",
    "DomainName",
    "DomainNameHasDNSRecord",
    "Exploit",
    "ExploitExploitsVulnerability",
    "Host",
    "IntrusionSet",
    "IntrusionSetAttributedToNation",
    "IntrusionSetLinkedToIntrusionSet",
    "IntrusionSetLinkedToMitreAttackGroup",
    "IntrusionSetIsOfType",
    "IntrusionSetLinkedToThreatActor",
    "IntrusionSetUsesSoftware",
    "IntrusionSetUsesTechnique",
    "IPAddressNode",
    "IPAddressBelongsToASN",
    "IPAddressHasOpenPort",
    "IPAddressIdentifiedAsPlatform",
    "IPAddressLocatedInCountry",
    "IPAddressMapsToMACAddress",
    "IPAddressObservedWithHostname",
    "JarmHash",
    "ListeningSocket",
    "ListeningSocketUsesPort",
    "ServiceIdentifiedAsPlatform",
    "MACAddress",
    "MACAddressAssignedToHost",
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
    "MitreAttackDataComponent",
    "MitreAttackDataComponentDetectsTechnique",
    "MitreAttackDataSource",
    "MitreAttackDataSourceHasComponent",
    "MitreAttackMitigation",
    "MitreAttackMitigationDefendsAgainstTechnique",
    "MitreAttackGroup",
    "MitreAttackGroupUsesSoftware",
    "MitreAttackGroupUsesTechnique",
    "NetworkService",
    "NetworkServiceRunsOnPort",
    "OpenPortHasJarmHash",
    "OpenPortPresentsBanner",
    "OpenPortPresentsX509Certificate",
    "Organisation",
    "OrganisationAssignedCVSSToCVE",
    "OrganisationPublishedThreatReport",
    "OrganisationReportedExploitationOfCVE",
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
    "UserAccount",
    "UserAccountAuthorizedOnHost",
]
