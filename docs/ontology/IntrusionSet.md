
# IntrusionSet

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| unique_id | str | True |
| name | str | True |
| description | Optional | False |
| url_reference | Optional | False |
| additional_urls | Optional | False |



## Outgoing Relationships

### INTRUSION_SET_LINKED_TO_THREAT_ACTOR

Target Label: ThreatActor

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | ThreatActor | True |
| source | IntrusionSet | True |
| url_reference | Optional | False |


### INTRUSION_SET_USES_SOFTWARE

Target Label: MitreAttackSoftware

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | MitreAttackSoftware | True |
| source | IntrusionSet | True |


### INTRUSION_SET_IS_OF_TYPE

Target Label: ActorType

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | ActorType | True |
| source | IntrusionSet | True |
| url_reference | Optional | False |


### INTRUSION_SET_ATTRIBUTED_TO_NATION

Target Label: Country

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Country | True |
| source | IntrusionSet | True |
| url_reference | Optional | False |


### INTRUSION_SET_LINKED_TO_INTRUSION_SET

Target Label: IntrusionSet

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | IntrusionSet | True |
| source | IntrusionSet | True |
| url_reference | Optional | False |


### INTRUSION_SET_USES_TECHNIQUE

Target Label: MitreAttackTechnique

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | MitreAttackTechnique | True |
| source | IntrusionSet | True |


### INTRUSION_SET_LINKED_TO_MITRE_ATTACK_GROUP

Target Label: MitreAttackGroup

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | MitreAttackGroup | True |
| source | IntrusionSet | True |




