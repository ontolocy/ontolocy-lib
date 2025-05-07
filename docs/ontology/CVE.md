# CVE

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| cve_id | str | True |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| published_date | Optional[datetime] | False |
| assigner | Optional[str] | False |
| description | Optional[str] | False |

## Relationships

### CVE_RELATES_TO_CWE

Target Label(s): CWE

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### CVE_RELATES_TO_CPE

Target Label(s): CPE

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |
| cpe | Optional[Annotated] | False |