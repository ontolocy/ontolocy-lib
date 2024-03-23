
# DNSRecord

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| content | str | True |
| name | str | True |
| type | str | True |
| unique_id | Optional | False |



## Outgoing Relationships

### DNS_RECORD_POINTS_TO_DOMAIN_NAME

Target Label: DomainName

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| observation_date | datetime | True |
| target | DomainName | True |
| source | DNSRecord | True |


### DNS_RECORD_POINTS_TO_IP_ADDRESS

Target Label: IPAddress

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| observation_date | datetime | True |
| target | IPAddressNode | True |
| source | DNSRecord | True |


### DNS_RECORD_FOR_DOMAIN

Target Label: DomainName

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| observation_date | datetime | True |
| target | DomainName | True |
| source | DNSRecord | True |




