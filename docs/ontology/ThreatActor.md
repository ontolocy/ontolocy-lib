# ThreatActor

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| url_reference | Optional[Annotated] | True |
| description | Optional[str] | True |
| unique_id | str | True |
| name | str | True |
| merged | datetime | False |
| created | Optional[datetime] | False |
| additional_urls | Optional[List[typing] | False |

## Relationships

### THREAT_ACTOR_LINKED_TO_THREAT_ACTOR

Target Label(s): ThreatActor

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |
| url_reference | Optional[Annotated] | False |
| context | Optional[str] | False |



### THREAT_ACTOR_ATTRIBUTED_TO_NATION

Target Label(s): Country

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |
| url_reference | Optional[Annotated] | False |



### THREAT_ACTOR_IS_OF_TYPE

Target Label(s): ActorType

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |
| url_reference | Optional[Annotated] | False |