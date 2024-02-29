
# ListeningSocket

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ip_address | IPvAnyAddress | True |
| port_number | int | True |
| protocol | ListeningSocketProtocolEnum | True |
| private | Optional | False |
| namespace | Optional | False |
| ip_address_unique_id | Optional | False |
| unique_id | Optional | False |



## Outgoing Relationships

### OPEN_PORT_PRESENTS_X509_CERTIFICATE

Target Label: X509Certificate

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | X509Certificate | True |
| source | ListeningSocket | True |


### OPEN_PORT_HAS_JARM_HASH

Target Label: JarmHash

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | JarmHash | True |
| source | ListeningSocket | True |


### SERVICE_HOSTS_URL

Target Label: URL

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | URLNode | True |
| source | ListeningSocket | True |
| status_code | Optional | False |


### LISTENING_SOCKET_USES_PORT

Target Label: Port

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Port | True |
| source | ListeningSocket | True |


### SERVICE_IDENTIFIED_AS_PLATFORM

Target Label: CPE

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| cpe | Optional | True |
| target | CPE | True |
| source | ListeningSocket | True |
| status_code | Optional | False |


### OPEN_PORT_PRESENTS_BANNER

Target Label: Banner

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Banner | True |
| source | ListeningSocket | True |




