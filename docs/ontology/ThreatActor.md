
# ThreatActor

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| unique_id | str | True |
| name | str | True |
| description | str | False |
| url_reference | HttpUrl | False |


## Outgoing Relationships

### THREAT_ACTOR_LINKED_TO_THREAT_ACTOR

Target Label: ThreatActor

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | ThreatActor | True |
| source | ThreatActor | True |
| url_reference | HttpUrl | False |
| context | str | False |


### THREAT_ACTOR_ATTRIBUTED_TO_NATION

Target Label: Country

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Country | True |
| source | ThreatActor | True |
| url_reference | HttpUrl | False |


### THREAT_ACTOR_IS_OF_TYPE

Target Label: ActorType

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | ActorType | True |
| source | ThreatActor | True |
| url_reference | HttpUrl | False |



