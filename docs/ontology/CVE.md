
# CVE

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| cve_id | str | True |
| published_date | Optional | False |
| assigner | Optional | False |
| description | Optional | False |



## Outgoing Relationships

### CVE_RELATES_TO_CPE

Target Label: CPE

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | CPE | True |
| source | CVE | True |
| cpe | Optional | False |


### CVE_RELATES_TO_CWE

Target Label: CWE

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | CWE | True |
| source | CVE | True |




