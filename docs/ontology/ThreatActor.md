
# ThreatActor

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| url_reference | Optional | True |
| description | Optional | True |
| unique_id | str | True |
| name | str | True |



## Outgoing Relationships

### THREAT_ACTOR_IS_OF_TYPE

Target Label: ActorType

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| url_reference | Optional | True |
| target | ActorType | True |
| source | ThreatActor | True |


### THREAT_ACTOR_ATTRIBUTED_TO_NATION

Target Label: Country

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| url_reference | Optional | True |
| target | Country | True |
| source | ThreatActor | True |


### THREAT_ACTOR_LINKED_TO_THREAT_ACTOR

Target Label: ThreatActor

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| context | Optional | True |
| url_reference | Optional | True |
| target | ThreatActor | True |
| source | ThreatActor | True |




