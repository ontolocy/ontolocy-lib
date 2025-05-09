# Incident

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| incident_date | date | True |
| unique_id | str | True |
| name | str | True |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| summary | Optional[str] | False |
| impact | Optional[str] | False |
| cost_usd | Optional[int] | False |
| url_reference | Optional[Annotated] | False |
| additional_urls | Optional[List[typing] | False |

## Relationships

### INCIDENT_AFFECTED_SECTOR

Target Label(s): Sector

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |
| url_reference | Optional[Annotated] | False |



### INCIDENT_LINKED_TO_INTRUSION_SET

Target Label(s): IntrusionSet

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |
| url_reference | Optional[Annotated] | False |



### INCIDENT_REFERENCED_BY_REPORT

Target Label(s): Report

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### INCIDENT_LINKED_TO_THREAT_ACTOR

Target Label(s): ThreatActor

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| ontolocy_merged | datetime | False |
| ontolocy_created | Optional[datetime] | False |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |
| url_reference | Optional[Annotated] | False |