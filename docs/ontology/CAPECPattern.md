# CAPECPattern

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| name | str | True |
| capec_id | int | True |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| description | Optional[str] | False |
| likelihood_of_attack | Optional[str] | False |
| typical_severity | Optional[str] | False |
| status | Optional[str] | False |

## Relationships

### CAPEC_PATTERN_RELATES_TO_CWE

Target Label(s): CWE

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### CAPEC_PATTERN_MAPS_TO_ATTACK_TECHNIQUE

Target Label(s): MitreAttackTechnique

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |