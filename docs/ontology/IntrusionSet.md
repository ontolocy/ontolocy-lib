# IntrusionSet

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| unique_id | str | True |
| name | str | True |
| merged | datetime | False |
| created | Optional[datetime] | False |
| description | Optional[str] | False |
| url_reference | Optional[Annotated] | False |
| additional_urls | Optional[List[typing] | False |

## Relationships

### INTRUSION_SET_LINKED_TO_MITRE_ATTACK_GROUP

Target Label(s): MitreAttackGroup

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |
| url_reference | Optional[Annotated] | False |



### INTRUSION_SET_LINKED_TO_INTRUSION_SET

Target Label(s): IntrusionSet

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |
| url_reference | Optional[Annotated] | False |



### INTRUSION_SET_USES_SOFTWARE

Target Label(s): MitreAttackSoftware

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### INTRUSION_SET_ATTRIBUTED_TO_NATION

Target Label(s): Country

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |
| url_reference | Optional[Annotated] | False |



### INTRUSION_SET_IS_OF_TYPE

Target Label(s): ActorType

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |
| url_reference | Optional[Annotated] | False |



### INTRUSION_SET_AFFILIATED_WITH_INTRUSION_SET

Target Label(s): IntrusionSet

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |
| url_reference | Optional[Annotated] | False |
| context | Optional[str] | False |



### INTRUSION_SET_LINKED_TO_THREAT_ACTOR

Target Label(s): ThreatActor

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |
| url_reference | Optional[Annotated] | False |



### INTRUSION_SET_USES_TECHNIQUE

Target Label(s): MitreAttackTechnique

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |