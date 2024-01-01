
# CAPECPattern

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| name | str | True |
| capec_id | int | True |
| description | Optional | False |
| likelihood_of_attack | Optional | False |
| typical_severity | Optional | False |



## Outgoing Relationships

### CAPEC_PATTERN_MAPS_TO_ATTACK_TECHNIQUE

Target Label: MitreAttackTechnique

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | MitreAttackTechnique | True |
| source | CAPECPattern | True |


### CAPEC_PATTERN_RELATES_TO_CWE

Target Label: CWE

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | CWE | True |
| source | CAPECPattern | True |




