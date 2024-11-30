# Campaign

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| unique_id | str | True |
| summary | Optional[str] | True |
| activity_datetime | datetime | True |
| url_reference | Url | True |
| title | str | True |
| merged | datetime | False |
| created | Optional[datetime] | False |

## Relationships

### CAMPAIGN_TARGETS_SECTOR

Target Label(s): Sector

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| url_reference | Optional[Annotated] | True |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### CAMPAIGN_TARGETS_COUNTRY

Target Label(s): Country

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| url_reference | Optional[Annotated] | True |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### CAMPAIGN_USES_TECHNIQUE

Target Label(s): MitreAttackTechnique

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| url_reference | Optional[Annotated] | True |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### CAMPAIGN_USES_CVE

Target Label(s): CVE

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| url_reference | Optional[Annotated] | True |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### CAMPAIGN_BY_INTRUSION_SET

Target Label(s): IntrusionSet

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| url_reference | Optional[Annotated] | True |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### CAMPAIGN_CAUSED_CYBER_HARM

Target Label(s): CyberHarm

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| url_reference | Optional[Annotated] | True |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |