
# MitreAttackGroup

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
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
| description | Optional | False |



## Outgoing Relationships

### MITRE_ATTACK_GROUP_USES_SOFTWARE

Target Label: MitreAttackSoftware

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | MitreAttackSoftware | True |
| source | MitreAttackGroup | True |


### MITRE_ATTACK_GROUP_USES_TECHNIQUE

Target Label: MitreAttackTechnique

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | MitreAttackTechnique | True |
| source | MitreAttackGroup | True |




