
# CobaltStrikeBeacon

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| submituri | str | True |
| useragent | str | True |
| c2server | str | True |
| jitter | int | True |
| maxgetsize | int | True |
| sleeptime | int | True |
| port | int | True |
| beacontype | int | True |
| watermark | int | False |
| unique_id | UUID | False |


## Outgoing Relationships

### COBALT_STRIKE_BEACON_HAS_WATERMARK

Target Label: CobaltStrikeWatermark

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | CobaltStrikeWatermark | True |
| source | CobaltStrikeBeacon | True |


### COBALT_STRIKE_BEACON_COLLECTED_FROM

Target Label: ListeningSocket

#### Relationship Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| target | ListeningSocket | True |
| source | CobaltStrikeBeacon | True |



