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
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |

## Relationships

### ASN_HAS_REGISTERED_CONTACT

Target Label(s): Organisation

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |