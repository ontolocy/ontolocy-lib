from typing import Any, ClassVar, Dict, Optional
from uuid import UUID

from pydantic import AnyHttpUrl, validator

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from ..utils import generate_deterministic_uuid
from .mitreattacktechnique import MitreAttackTechnique


class Control(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "Control"

    control_id: str
    name: str
    version: Optional[str]
    framework: str
    framework_version: Optional[str]
    description: Optional[str]
    context: Optional[str]
    unique_id: Optional[str]
    url_reference: Optional[AnyHttpUrl]

    @validator("unique_id", always=True)
    def generate_uuid(cls, v: Optional[UUID], values: Dict[str, Any]) -> UUID:
        if v is None:
            key_values = [
                values["control_id"],
                values["version"],
                values["framework"],
                values["framework_version"],
            ]

            v = generate_deterministic_uuid(key_values)

        return v

    def __str__(self) -> str:
        return f"{self.name} ({self.framework})"


#
# OUTGOING RELATIONSHIPS
#


class ControlRelatedToControl(OntolocyRelationship):
    source: Control
    target: Control

    context: Optional[str]
    url_reference: Optional[AnyHttpUrl]

    __relationshiptype__: ClassVar[str] = "CONTROL_RELATED_TO_CONTROL"


class ControlHasParentControl(OntolocyRelationship):
    source: Control
    target: Control

    context: Optional[str]
    url_reference: Optional[AnyHttpUrl]

    __relationshiptype__: ClassVar[str] = "CONTROL_HAS_PARENT_CONTROL"


class ControlMitigatesAttackTechnique(OntolocyRelationship):
    source: Control
    target: MitreAttackTechnique

    url_reference: Optional[AnyHttpUrl]

    __relationshiptype__: ClassVar[str] = "CONTROL_MITIGATES_ATTACK_TECHNIQUE"
