# NetworkService

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| name | str | True |
| merged | datetime | False |
| created | Optional[datetime] | False |
| description | Optional[str] | False |

## Relationships

### NETWORK_SERVICE_RUNS_ON_PORT

Target Label(s): Port

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |