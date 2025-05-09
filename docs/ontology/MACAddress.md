# MACAddress

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| mac_address | str | True |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |

## Relationships

### MAC_ADDRESS_ASSIGNED_TO_HOST

Target Label(s): Host

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |
| interface | Optional[str] | False |