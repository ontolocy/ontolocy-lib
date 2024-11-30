# ControlValidationTest

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| framework | str | True |
| name | str | True |
| test_id | str | True |
| merged | datetime | False |
| created | Optional[datetime] | False |
| version | Optional[str] | False |
| framework_version | Optional[str] | False |
| description | Optional[str] | False |
| context | Optional[str] | False |
| unique_id | Optional[str] | False |
| url_reference | Optional[Annotated] | False |
| platform_tags | Optional[List[str]] | False |

## Relationships

### CONTROL_VALIDATION_TEST_FOR_ATTACK_TECHNIQUE

Target Label(s): MitreAttackTechnique

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |