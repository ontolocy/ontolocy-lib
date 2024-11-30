# DNSRecord

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| content | str | True |
| name | str | True |
| type | str | True |
| merged | datetime | False |
| created | Optional[datetime] | False |
| unique_id | Optional[UUID] | False |

## Relationships

### DNS_RECORD_POINTS_TO_IP_ADDRESS

Target Label(s): IPAddress

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| observation_date | datetime | True |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### DNS_RECORD_FOR_DOMAIN

Target Label(s): DomainName

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| observation_date | datetime | True |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### DNS_RECORD_POINTS_TO_DOMAIN_NAME

Target Label(s): DomainName

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| observation_date | datetime | True |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |