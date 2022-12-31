
# Organisation

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| name | str | True |
| address | str | False |


## Outgoing Relationships

### ORGANISATION_ASSIGNED_CVSS_TO_CVE

Target Label: CVE

#### Relationship Properties

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
| target | CVE | True |
| source | Organisation | True |



