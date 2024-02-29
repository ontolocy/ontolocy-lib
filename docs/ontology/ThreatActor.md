
# ThreatActor

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| url_reference | Optional | True |
| description | Optional | True |
| unique_id | str | True |
| name | str | True |
| additional_urls | Optional | False |



## Outgoing Relationships

### THREAT_ACTOR_ATTRIBUTED_TO_NATION

Target Label: Country

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Country | True |
| source | ThreatActor | True |
| url_reference | Optional | False |


### THREAT_ACTOR_LINKED_TO_THREAT_ACTOR

Target Label: ThreatActor

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | ThreatActor | True |
| source | ThreatActor | True |
| url_reference | Optional | False |
| context | Optional | False |


### THREAT_ACTOR_IS_OF_TYPE

Target Label: ActorType

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | ActorType | True |
| source | ThreatActor | True |
| url_reference | Optional | False |




