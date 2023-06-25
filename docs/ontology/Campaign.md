
# Campaign

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| unique_id | str | True |
| activity_datetime | datetime | True |
| url_reference | HttpUrl | True |
| title | str | True |
| summary | str | False |


## Outgoing Relationships

### CAMPAIGN_TARGETS_COUNTRY

Target Label: Country

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Country | True |
| source | Campaign | True |
| url_reference | HttpUrl | False |


### CAMPAIGN_TARGETS_SECTOR

Target Label: Sector

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Sector | True |
| source | Campaign | True |
| url_reference | HttpUrl | False |


### CAMPAIGN_CAUSED_CYBER_HARM

Target Label: CyberHarm

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | CyberHarm | True |
| source | Campaign | True |
| url_reference | HttpUrl | False |


### CAMPAIGN_BY_INTRUSION_SET

Target Label: IntrusionSet

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | IntrusionSet | True |
| source | Campaign | True |
| url_reference | HttpUrl | False |


### CAMPAIGN_USES_TECHNIQUE

Target Label: MitreAttackTechnique

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | MitreAttackTechnique | True |
| source | Campaign | True |
| url_reference | HttpUrl | False |


### CAMPAIGN_USES_CVE

Target Label: CVE

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | CVE | True |
| source | Campaign | True |
| url_reference | HttpUrl | False |



