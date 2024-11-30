# IPAddress

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ip_address | IPvAnyAddress | True |
| merged | datetime | False |
| created | Optional[datetime] | False |
| ip_version | Optional[Enum] | False |
| private | Optional[bool] | False |
| namespace | Optional[str] | False |
| unique_id | Optional[str] | False |

## Relationships

### IP_ADDRESS_BELONGS_TO_ASN

Target Label(s): ASN

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### IP_ADDRESS_HAS_OPEN_PORT

Target Label(s): ListeningSocket

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### IP_ADDRESS_MAPS_TO_MAC_ADDRESS

Target Label(s): MACAddress

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### IP_ADDRESS_IDENTIFIED_AS_PLATFORM

Target Label(s): CPE

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### IP_ADDRESS_LOCATED_IN_COUNTRY

Target Label(s): Country

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### IP_ADDRESS_OBSERVED_WITH_HOSTNAME

Target Label(s): DomainName

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |