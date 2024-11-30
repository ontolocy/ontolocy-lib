# MitreAttackTactic

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| description | str | True |
| name | str | True |
| ref_url | Url | True |
| attack_shortname | str | True |
| attack_version | str | True |
| attack_spec_version | str | True |
| attack_id | str | True |
| stix_modified | datetime | True |
| stix_created | datetime | True |
| stix_type | str | True |
| stix_id | str | True |
| merged | datetime | False |
| created | Optional[datetime] | False |
| stix_spec_version | str | False |
| stix_revoked | Optional[bool] | False |
| attack_deprecated | Optional[bool] | False |

## Relationships

### MITRE_TACTIC_INCLUDES_TECHNIQUE

Target Label(s): MitreAttackTechnique

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |