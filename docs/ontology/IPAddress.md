
# IPAddress

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ip_address | IPvAnyAddress | True |
| ip_version | IPVersionEnum | False |
| private | bool | False |
| namespace | str | False |
| unique_id | UUID | False |


## Outgoing Relationships

### IP_ADDRESS_HAS_OPEN_PORT

Target Label: ListeningSocket

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | ListeningSocket | True |
| source | IPAddressNode | True |


### IP_ADDRESS_LOCATED_IN_COUNTRY

Target Label: Country

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Country | True |
| source | IPAddressNode | True |


### IP_ADDRESS_BELONGS_TO_ASN

Target Label: ASN

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | ASN | True |
| source | IPAddressNode | True |



