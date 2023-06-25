
# Control

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| framework | str | True |
| name | str | True |
| control_id | str | True |
| version | str | False |
| framework_version | str | False |
| description | str | False |
| context | str | False |
| unique_id | str | False |


## Outgoing Relationships

### CONTROL_MITIGATES_ATTACK_TECHNIQUE

Target Label: MitreAttackTechnique

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | MitreAttackTechnique | True |
| source | Control | True |
| url_reference | AnyHttpUrl | False |


### CONTROL_RELATED_TO_CONTROL

Target Label: Control

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | Control | True |
| source | Control | True |
| url_reference | AnyHttpUrl | False |



