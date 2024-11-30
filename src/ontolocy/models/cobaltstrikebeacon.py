from typing import ClassVar, Optional

from pydantic import ValidationInfo, field_validator

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from ..utils import generate_deterministic_uuid
from .cobaltstrikewatermark import CobaltStrikeWatermark
from .listeningsocket import ListeningSocket


class CobaltStrikeBeacon(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "CobaltStrikeBeacon"

    beacontype: int
    port: int
    sleeptime: int
    maxgetsize: int
    jitter: int
    c2server: str
    useragent: Optional[str] = None
    submituri: Optional[str] = None
    watermark: Optional[int] = None

    unique_id: Optional[str] = None

    @field_validator("unique_id")
    def generate_uuid(cls, v: Optional[str], info: ValidationInfo) -> str:
        values = info.data
        if v is None:
            key_values = [
                values["beacontype"],
                values["port"],
                values["c2server"],
                values["watermark"],
            ]

            v = str(generate_deterministic_uuid(key_values))

        return v


class CobaltStikeBeaconCollectedFrom(OntolocyRelationship):
    __relationshiptype__: ClassVar[str] = "COBALT_STRIKE_BEACON_COLLECTED_FROM"

    source: CobaltStrikeBeacon
    target: ListeningSocket


class CobaltStikeBeaconHasWatermark(OntolocyRelationship):
    __relationshiptype__: ClassVar[str] = "COBALT_STRIKE_BEACON_HAS_WATERMARK"

    source: CobaltStrikeBeacon
    target: CobaltStrikeWatermark
