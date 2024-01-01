
# UserAccount

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| username | str | True |
| local_hostname | Optional | False |
| namespace | Optional | False |
| unique_id | Optional | False |



## Outgoing Relationships

### USER_ACCOUNT_AUTHORIZED_ON_HOST

Target Label: Host

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Host | True |
| source | UserAccount | True |




