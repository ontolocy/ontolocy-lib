
# NetworkService

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| name | str | True |
| description | Optional | False |



## Outgoing Relationships

### NETWORK_SERVICE_RUNS_ON_PORT

Target Label: Port

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Port | True |
| source | NetworkService | True |




