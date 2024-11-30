# Detection

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| framework | str | True |
| name | str | True |
| detection_id | str | True |
| merged | datetime | False |
| created | Optional[datetime] | False |
| version | Optional[str] | False |
| framework_version | Optional[str] | False |
| description | Optional[str] | False |
| context | Optional[str] | False |
| unique_id | Optional[str] | False |
| url_reference | Optional[Annotated] | False |
| source_tags | Optional[List[str]] | False |

## Relationships

### DETECTION_FOR_ATTACK_TECHNIQUE

Target Label(s): MitreAttackTechnique

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |