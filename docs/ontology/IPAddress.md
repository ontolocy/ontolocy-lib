
# IPAddress

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ip_address | IPvAnyAddress | True |
| ip_version | Optional | False |
| private | Optional | False |
| namespace | Optional | False |
| unique_id | Optional | False |



## Outgoing Relationships

### IP_ADDRESS_IDENTIFIED_AS_PLATFORM

Target Label: CPE

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | CPE | True |
| source | IPAddressNode | True |


### IP_ADDRESS_LOCATED_IN_COUNTRY

Target Label: Country

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Country | True |
| source | IPAddressNode | True |


### IP_ADDRESS_MAPS_TO_MAC_ADDRESS

Target Label: MACAddress

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | MACAddress | True |
| source | IPAddressNode | True |


### IP_ADDRESS_OBSERVED_WITH_HOSTNAME

Target Label: DomainName

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | DomainName | True |
| source | IPAddressNode | True |


### IP_ADDRESS_HAS_OPEN_PORT

Target Label: ListeningSocket

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | ListeningSocket | True |
| source | IPAddressNode | True |


### IP_ADDRESS_BELONGS_TO_ASN

Target Label: ASN

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | ASN | True |
| source | IPAddressNode | True |




