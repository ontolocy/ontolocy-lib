# CobaltStrikeBeacon

## Node Properties

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| c2server | str | True |
| jitter | int | True |
| maxgetsize | int | True |
| sleeptime | int | True |
| port | int | True |
| beacontype | int | True |
| merged | datetime | False |
| created | Optional[datetime] | False |
| useragent | Optional[str] | False |
| submituri | Optional[str] | False |
| watermark | Optional[int] | False |
| unique_id | Optional[str] | False |

## Relationships

### COBALT_STRIKE_BEACON_COLLECTED_FROM

Target Label(s): ListeningSocket

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |



### COBALT_STRIKE_BEACON_HAS_WATERMARK

Target Label(s): CobaltStrikeWatermark

| Property Name | Type | Required |
| ------------- | ---- | -------- |
| data_origin_name | Optional[str] | False |
| data_origin_reference | Optional[str] | False |
| data_origin_license | Optional[str] | False |
| data_origin_sharing | Optional[str] | False |