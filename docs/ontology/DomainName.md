# DomainName

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| name | str | True |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |

## Relationships

### DOMAIN_NAME_HAS_DNS_RECORD

Target Label(s): DNSRecord

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| observation_date | datetime | True |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |