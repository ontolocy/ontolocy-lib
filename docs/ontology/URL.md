# URL

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| url | Url | True |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |

## Relationships

### URL_REDIRECTS_TO_URL

Target Label(s): URL

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |