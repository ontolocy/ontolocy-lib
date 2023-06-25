
# MitreAttackCampaign

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| description | str | True |
| name | str | True |
| ref_url | HttpUrl | True |
| attack_id | str | True |
| attack_last_seen_citation | str | True |
| attack_first_seen_citation | str | True |
| attack_version | str | True |
| attack_spec_version | str | True |
| stix_last_seen | datetime | True |
| stix_first_seen | datetime | True |
| stix_modified | datetime | True |
| stix_created | datetime | True |
| stix_type | str | True |
| stix_id | str | True |
| stix_spec_version | str | False |
| stix_revoked | bool | False |


## Outgoing Relationships

### MITRE_CAMPAIGN_USES_TECHNIQUE

Target Label: MitreAttackTechnique

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | MitreAttackTechnique | True |
| source | MitreAttackCampaign | True |


### MITRE_CAMPAIGN_USES_SOFTWARE

Target Label: MitreAttackSoftware

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | MitreAttackSoftware | True |
| source | MitreAttackCampaign | True |


### MITRE_CAMPAIGN_ATTRIBUTED_TO_INTRUSION_SET

Target Label: IntrusionSet

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | IntrusionSet | True |
| source | MitreAttackCampaign | True |



