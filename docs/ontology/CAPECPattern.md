
# CAPECPattern

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| name | str | True |
| capec_id | int | True |
| description | str | False |
| likelihood_of_attack | str | False |
| typical_severity | str | False |


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



