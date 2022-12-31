
# CVE

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| cve_id | ConstrainedStrValue | True |
| published_date | datetime | False |
| assigner | str | False |


## Outgoing Relationships

### CVE_RELATES_TO_CPE

Target Label: CPE

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | CPE | True |
| source | CVE | True |


### CVE_RELATES_TO_CWE

Target Label: CWE

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | CWE | True |
| source | CVE | True |



