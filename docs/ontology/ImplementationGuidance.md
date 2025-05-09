# ImplementationGuidance

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| framework | str | True |
| guidance_id | str | True |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| name | Optional[str] | False |
| effectiveness | Optional[Enum] | False |
| version | Optional[str] | False |
| framework_version | Optional[str] | False |
| description | Optional[str] | False |
| context | Optional[str] | False |
| unique_id | Optional[str] | False |
| url_reference | Optional[Annotated] | False |

## Relationships

### IMPLEMENTATION_GUIDANCE_FOR_CONTROL

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



### IMPLEMENTATION_GUIDANCE_FOR_IMPLEMENTATION_GUIDANCE

Target Label(s): ImplementationGuidance

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