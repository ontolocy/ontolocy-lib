from typing import ClassVar, Optional

from pydantic import AnyHttpUrl, ValidationInfo, field_serializer, field_validator

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from ..utils import generate_str_id
from .mitreattacktechnique import MitreAttackTechnique


class Control(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "Control"

    control_id: str
    name: str
    framework: str
    framework_level: Optional[str] = None
    version: Optional[str] = None
    framework_version: Optional[str] = None
    description: Optional[str] = None
    context: Optional[str] = None
    unique_id: Optional[str] = None
    url_reference: Optional[AnyHttpUrl] = None

    def __str__(self) -> str:
        return f"{self.control_id}: {self.name}"

    @field_validator("unique_id")
    def generate_id(cls, v: Optional[str], info: ValidationInfo) -> str:
        values = info.data
        if v is None:
            key_values = [
                values["framework"],
                values["framework_level"],
                values["framework_version"],
                values["control_id"],
                values["version"],
            ]

            # the unique id should be a string rather than a UUID
            v = generate_str_id(key_values)

        return v

    @field_serializer("url_reference")
    def serialize_to_str(self, input: AnyHttpUrl, _info):
        if input:
            return str(input)


#
# OUTGOING RELATIONSHIPS
#


class ControlRelatedToControl(OntolocyRelationship):
    source: Control
    target: Control

    context: Optional[str] = None
    url_reference: Optional[AnyHttpUrl] = None

    __relationshiptype__: ClassVar[str] = "CONTROL_RELATED_TO_CONTROL"

    @field_serializer("url_reference")
    def serialize_to_str(self, input: AnyHttpUrl, _info):
        if input:
            return str(input)


class ControlHasParentControl(OntolocyRelationship):
    source: Control
    target: Control

    context: Optional[str] = None
    url_reference: Optional[AnyHttpUrl] = None

    __relationshiptype__: ClassVar[str] = "CONTROL_HAS_PARENT_CONTROL"

    @field_serializer("url_reference")
    def serialize_to_str(self, input: AnyHttpUrl, _info):
        if input:
            return str(input)


class ControlMitigatesAttackTechnique(OntolocyRelationship):
    source: Control
    target: MitreAttackTechnique

    url_reference: Optional[AnyHttpUrl] = None

    __relationshiptype__: ClassVar[str] = "CONTROL_MITIGATES_ATTACK_TECHNIQUE"

    @field_serializer("url_reference")
    def serialize_to_str(self, input: AnyHttpUrl, _info):
        if input:
            return str(input)
