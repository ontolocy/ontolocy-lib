
# ASN

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| registry | str | True |
| country_code | str | True |
| cidr | IPvAnyNetwork | True |
| description | str | True |
| network_name | str | True |
| number | int | True |


## Outgoing Relationships

### ASN_HAS_REGISTERED_CONTACT

Target Label: Organisation

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Organisation | True |
| source | ASN | True |



