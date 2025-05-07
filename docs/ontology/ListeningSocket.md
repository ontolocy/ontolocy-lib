# ListeningSocket

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ip_address | IPvAnyAddress | True |
| port_number | int | True |
| protocol | Enum | True |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| private | Optional[bool] | False |
| namespace | Optional[str] | False |
| ip_address_unique_id | Optional[str] | False |
| unique_id | Optional[str] | False |

## Relationships

### LISTENING_SOCKET_USES_PORT

Target Label(s): Port

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### LISTENING_SOCKET_HAS_BANNER

Target Label(s): Banner

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### LISTENING_SOCKET_HAS_X509_CERTIFICATE

Target Label(s): X509Certificate

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### LISTENING_SOCKET_HAS_JARM_HASH

Target Label(s): JarmHash

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### LISTENING_SOCKET_IDENTIFIED_AS_PLATFORM

Target Label(s): CPE

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| cpe | Optional[Annotated] | True |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |
| status_code | Optional[int] | False |



### LISTENING_SOCKET_HOSTS_URL

Target Label(s): URL

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |
| status_code | Optional[int] | False |