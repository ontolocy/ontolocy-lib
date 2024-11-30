# Organisation

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| name | str | True |
| merged | datetime | False |
| created | Optional[datetime] | False |
| description | Optional[str] | False |
| address | Optional[str] | False |

## Relationships

### ORGANISATION_REPORTED_EXPLOITATION_OF_CVE

Target Label(s): CVE

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| required_action | Optional[str] | True |
| description | Optional[str] | True |
| url_reference | Optional[Annotated] | True |
| reported_date | date | True |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### ORGANISATION_ASSIGNED_CVSS_TO_CVE

Target Label(s): CVE

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| impact_score | float | True |
| exploitability_score | float | True |
| base_severity | str | True |
| base_score | float | True |
| availability_impact | str | True |
| integrity_impact | str | True |
| confidentiality_impact | str | True |
| scope | str | True |
| user_interaction | str | True |
| privileges_required | str | True |
| attack_complexity | str | True |
| attack_vector | str | True |
| vector_string | str | True |
| version | str | True |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### ORGANISATION_PUBLISHED_THREAT_REPORT

Target Label(s): Report

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| url_reference | Optional[Annotated] | True |
| context | Optional[str] | True |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |