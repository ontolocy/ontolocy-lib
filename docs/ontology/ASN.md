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
| merged | datetime | False |
| created | Optional[datetime] | False |

## Relationships

### ASN_HAS_REGISTERED_CONTACT

Target Label(s): Organisation

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |