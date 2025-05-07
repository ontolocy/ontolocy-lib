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
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| stix_spec_version | str | False |
| stix_revoked | Optional[bool] | False |
| attack_deprecated | Optional[bool] | False |
| description | Optional[str] | False |

## Relationships

### MITRE_ATTACK_GROUP_USES_SOFTWARE

Target Label(s): MitreAttackSoftware

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### MITRE_ATTACK_GROUP_USES_TECHNIQUE

Target Label(s): MitreAttackTechnique

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |