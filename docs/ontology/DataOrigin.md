# DataOrigin

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| name | str | True |
| reference | Optional[str] | False |
| license | Optional[str] | False |
| sharing | Optional[str] | False |
| unique_id | Optional[UUID] | False |

## Relationships

### ORIGIN_GENERATED

Target Label(s): DataOrigin, ActorType, ASN, Organisation, CPE, CWE, CVE, Country, CyberHarm, MitreAttackTechnique, MitreAttackSoftware, MitreAttackGroup, ThreatActor, IntrusionSet, Sector, Campaign, Port, Banner, JarmHash, URL, X509Certificate, ListeningSocket, Host, MACAddress, IPAddress, DomainName, DNSRecord, Report, CAPECPattern, CobaltStrikeWatermark, CobaltStrikeBeacon, Control, ControlValidationTest, Detection, Exploit, MitreAttackCampaign, MitreAttackDataComponent, MitreAttackDataSource, MitreAttackMitigation, MitreAttackTactic, NetworkService, UserAccount