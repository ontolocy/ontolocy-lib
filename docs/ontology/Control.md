# Control

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| framework | str | True |
| name | str | True |
| control_id | str | True |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| framework_level | Optional[str] | False |
| version | Optional[str] | False |
| framework_version | Optional[str] | False |
| description | Optional[str] | False |
| context | Optional[str] | False |
| unique_id | Optional[str] | False |
| url_reference | Optional[Annotated] | False |

## Relationships

### CONTROL_MITIGATES_ATTACK_TECHNIQUE

Target Label(s): MitreAttackTechnique

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |
| url_reference | Optional[Annotated] | False |



### CONTROL_RELATED_TO_CONTROL

Target Label(s): Control

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |
| context | Optional[str] | False |
| url_reference | Optional[Annotated] | False |



### CONTROL_HAS_PARENT_CONTROL

Target Label(s): Control

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |
| context | Optional[str] | False |
| url_reference | Optional[Annotated] | False |