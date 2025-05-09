from enum import Enum
from typing import ClassVar, Optional

from pydantic import AnyHttpUrl, ValidationInfo, field_serializer, field_validator

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from ..utils import generate_deterministic_uuid
from .control import Control


class EffectivenessEnum(Enum):
    POSITIVE = "positive"
    INTERMEDIATE = "intermediate"
    NEGATIVE = "negative"


class ImplementationGuidance(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "ImplementationGuidance"

    guidance_id: str
    name: Optional[str] = None
    framework: str
    effectiveness: Optional[EffectivenessEnum] = None
    version: Optional[str] = None
    framework_version: Optional[str] = None
    description: Optional[str] = None
    context: Optional[str] = None
    unique_id: Optional[str] = None
    url_reference: Optional[AnyHttpUrl] = None

    def __str__(self) -> str:
        return f"{self.guidance_id}: {self.name}"

    @field_validator("unique_id")
    def generate_uuid(cls, v: Optional[str], info: ValidationInfo) -> str:
        values = info.data
        if v is None:
            key_values = [
                values["guidance_id"],
                values["version"],
                values["framework"],
                values["framework_version"],
            ]

            # the unique id should be a string rather than a UUID
            v = str(generate_deterministic_uuid(key_values))

        return v

    @field_serializer("url_reference")
    def serialize_to_str(self, input: AnyHttpUrl, _info):
        if input:
            return str(input)

    @field_serializer("effectiveness")
    def serialize_enum(self, input: EffectivenessEnum, _info):
        if input:
            return input.value


#
# OUTGOING RELATIONSHIPS
#


class ImplementationGuidanceForControl(OntolocyRelationship):
    source: ImplementationGuidance
    target: Control

    context: Optional[str] = None
    url_reference: Optional[AnyHttpUrl] = None

    __relationshiptype__: ClassVar[str] = "IMPLEMENTATION_GUIDANCE_FOR_CONTROL"

    @field_serializer("url_reference")
    def serialize_to_str(self, input: AnyHttpUrl, _info):
        if input:
            return str(input)


class ImplementationGuidanceForImplementationGuidance(OntolocyRelationship):
    source: ImplementationGuidance
    target: ImplementationGuidance

    context: Optional[str] = None
    url_reference: Optional[AnyHttpUrl] = None

    __relationshiptype__: ClassVar[str] = (
        "IMPLEMENTATION_GUIDANCE_FOR_IMPLEMENTATION_GUIDANCE"
    )

    @field_serializer("url_reference")
    def serialize_to_str(self, input: AnyHttpUrl, _info):
        if input:
            return str(input)
