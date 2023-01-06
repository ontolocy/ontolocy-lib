
# Report

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| published_date | date | True |
| url_reference | HttpUrl | True |
| author | str | True |
| title | str | True |
| summary | str | False |


## Outgoing Relationships

### REPORT_IDENTIFIES_VICTIM_SECTOR

Target Label: Sector

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Sector | True |
| source | Report | True |


### REPORT_MENTIONS_CVE

Target Label: CVE

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | CVE | True |
| source | Report | True |


### REPORT_MENTIONS_SECTOR

Target Label: Sector

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Sector | True |
| source | Report | True |


### REPORT_IDENTIFIES_CVE

Target Label: CVE

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | CVE | True |
| source | Report | True |


### REPORT_IDENTIFIES_TECHNIQUE

Target Label: MitreAttackTechnique

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | MitreAttackTechnique | True |
| source | Report | True |


### REPORT_IDENTIFIES_INTRUSION_SET

Target Label: IntrusionSet

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | IntrusionSet | True |
| source | Report | True |


### REPORT_IDENTIFIES_SOFTWARE

Target Label: MitreAttackSoftware

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | MitreAttackSoftware | True |
| source | Report | True |


### REPORT_IDENTIFIES_CAMPAIGN

Target Label: Campaign

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Campaign | True |
| source | Report | True |


### REPORT_IDENTIFIES_VICTIM_COUNTRY

Target Label: Country

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Country | True |
| source | Report | True |


### REPORT_IDENTIFIES_CYBER_HARM

Target Label: CyberHarm

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | CyberHarm | True |
| source | Report | True |


### REPORT_IDENTIFIES_SPONSOR_COUNTRY

Target Label: Country

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Country | True |
| source | Report | True |


### REPORT_MENTIONS_INTRUSION_SET

Target Label: IntrusionSet

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | IntrusionSet | True |
| source | Report | True |


### REPORT_MENTIONS_TECHNIQUE

Target Label: MitreAttackTechnique

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | MitreAttackTechnique | True |
| source | Report | True |


### REPORT_MENTIONS_COUNTRY

Target Label: Country

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Country | True |
| source | Report | True |


### REPORT_MENTIONS_IP

Target Label: IPAddress

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | IPAddressNode | True |
| source | Report | True |



