from typing import ClassVar, Optional
from uuid import UUID

from pydantic import AnyHttpUrl, ValidationInfo, field_validator

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from ..utils import generate_deterministic_uuid
from .mitreattacktechnique import MitreAttackTechnique


class Control(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "Control"

    control_id: str
    name: str
    framework: str
    version: Optional[str] = None
    framework_version: Optional[str] = None
    description: Optional[str] = None
    context: Optional[str] = None
    unique_id: Optional[str] = None
    url_reference: Optional[AnyHttpUrl] = None

    def __str__(self) -> str:
        return f"{self.control_id}: {self.name}"

    @field_validator("unique_id")
    def generate_uuid(cls, v: Optional[UUID], info: ValidationInfo) -> UUID:
        values = info.data
        if v is None:
            key_values = [
                values["control_id"],
                values["version"],
                values["framework"],
                values["framework_version"],
            ]

            # the unique id should be a string rather than a UUID
            v = str(generate_deterministic_uuid(key_values))

        return v


#
# OUTGOING RELATIONSHIPS
#


class ControlRelatedToControl(OntolocyRelationship):
    source: Control
    target: Control

    context: Optional[str] = None
    url_reference: Optional[AnyHttpUrl] = None

    __relationshiptype__: ClassVar[str] = "CONTROL_RELATED_TO_CONTROL"


class ControlHasParentControl(OntolocyRelationship):
    source: Control
    target: Control

    context: Optional[str] = None
    url_reference: Optional[AnyHttpUrl] = None

    __relationshiptype__: ClassVar[str] = "CONTROL_HAS_PARENT_CONTROL"


class ControlMitigatesAttackTechnique(OntolocyRelationship):
    source: Control
    target: MitreAttackTechnique

    url_reference: Optional[AnyHttpUrl] = None

    __relationshiptype__: ClassVar[str] = "CONTROL_MITIGATES_ATTACK_TECHNIQUE"
