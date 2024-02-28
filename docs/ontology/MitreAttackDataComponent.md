
# MitreAttackDataComponent

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| description | str | True |
| name | str | True |
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

### MITRE_ATTACK_DATA_COMPONENT_DETECTS_TECHNIQUE

Target Label: MitreAttackTechnique

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | MitreAttackTechnique | True |
| source | MitreAttackDataComponent | True |




