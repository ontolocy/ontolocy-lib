
# MitreAttackDataSource

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| description | str | True |
| name | str | True |
| ref_url | Url | True |
| attack_id | str | True |
| attack_version | str | True |
| attack_spec_version | str | True |
| stix_modified | datetime | True |
| stix_created | datetime | True |
| stix_type | str | True |
| stix_id | str | True |
| stix_spec_version | str | False |
| stix_revoked | Optional | False |
| attack_deprecated | Optional | False |



## Outgoing Relationships

### MITRE_ATTACK_DATA_SOURCE_HAS_COMPONENT

Target Label: MitreAttackDataComponent

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | MitreAttackDataComponent | True |
| source | MitreAttackDataSource | True |




