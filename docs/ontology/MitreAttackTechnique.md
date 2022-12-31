
# MitreAttackTechnique

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| description | str | True |
| name | str | True |
| ref_url | HttpUrl | True |
| attack_version | str | True |
| attack_spec_version | str | True |
| attack_id | ConstrainedStrValue | True |
| stix_modified | datetime | True |
| stix_created | datetime | True |
| stix_type | str | True |
| stix_id | str | True |
| stix_spec_version | str | False |
| stix_revoked | bool | False |
| attack_subtechnique | bool | False |


## Outgoing Relationships

### MITRE_SUBTECHNIQUE_OF

Target Label: MitreAttackTechnique

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | MitreAttackTechnique | True |
| source | MitreAttackTechnique | True |



