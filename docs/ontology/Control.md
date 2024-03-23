
# Control

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| framework | str | True |
| name | str | True |
| control_id | str | True |
| version | Optional | False |
| framework_version | Optional | False |
| description | Optional | False |
| context | Optional | False |
| unique_id | Optional | False |
| url_reference | Optional | False |



## Outgoing Relationships

### CONTROL_MITIGATES_ATTACK_TECHNIQUE

Target Label: MitreAttackTechnique

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | MitreAttackTechnique | True |
| source | Control | True |
| url_reference | Optional | False |


### CONTROL_RELATED_TO_CONTROL

Target Label: Control

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Control | True |
| source | Control | True |
| context | Optional | False |
| url_reference | Optional | False |


### CONTROL_HAS_PARENT_CONTROL

Target Label: Control

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Control | True |
| source | Control | True |
| context | Optional | False |
| url_reference | Optional | False |




