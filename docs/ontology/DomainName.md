
# DomainName

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| name | str | True |



## Outgoing Relationships

### DOMAIN_NAME_HAS_DNS_RECORD

Target Label: DNSRecord

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| observation_date | datetime | True |
| target | DNSRecord | True |
| source | DomainName | True |




