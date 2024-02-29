
# Campaign

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| unique_id | str | True |
| summary | Optional | True |
| activity_datetime | datetime | True |
| url_reference | Url | True |
| title | str | True |



## Outgoing Relationships

### CAMPAIGN_BY_INTRUSION_SET

Target Label: IntrusionSet

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| url_reference | Optional | True |
| target | IntrusionSet | True |
| source | Campaign | True |


### CAMPAIGN_USES_TECHNIQUE

Target Label: MitreAttackTechnique

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| url_reference | Optional | True |
| target | MitreAttackTechnique | True |
| source | Campaign | True |


### CAMPAIGN_TARGETS_COUNTRY

Target Label: Country

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| url_reference | Optional | True |
| target | Country | True |
| source | Campaign | True |


### CAMPAIGN_CAUSED_CYBER_HARM

Target Label: CyberHarm

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| url_reference | Optional | True |
| target | CyberHarm | True |
| source | Campaign | True |


### CAMPAIGN_TARGETS_SECTOR

Target Label: Sector

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| url_reference | Optional | True |
| target | Sector | True |
| source | Campaign | True |


### CAMPAIGN_USES_CVE

Target Label: CVE

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| url_reference | Optional | True |
| target | CVE | True |
| source | Campaign | True |




