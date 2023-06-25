
# MACAddress

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| mac_address | ConstrainedStrValue | True |


## Outgoing Relationships

### MAC_ADDRESS_ASSIGNED_TO_HOST

Target Label: Host

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Host | True |
| source | MACAddress | True |
| interface | str | False |



