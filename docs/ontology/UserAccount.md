# UserAccount

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| username | str | True |
| merged | datetime | False |
| created | Optional[datetime] | False |
| local_hostname | Optional[str] | False |
| namespace | Optional[str] | False |
| unique_id | Optional[UUID] | False |

## Relationships

### USER_ACCOUNT_AUTHORIZED_ON_HOST

Target Label(s): Host

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |