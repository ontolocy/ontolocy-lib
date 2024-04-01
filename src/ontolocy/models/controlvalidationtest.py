from typing import ClassVar, Optional

from pydantic import AnyHttpUrl, ValidationInfo, field_validator

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from ..utils import generate_deterministic_uuid
from .mitreattacktechnique import MitreAttackTechnique


class ControlValidationTest(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "ControlValidationTest"

    test_id: str
    name: str
    framework: str
    version: Optional[str] = None
    framework_version: Optional[str] = None
    description: Optional[str] = None
    context: Optional[str] = None
    unique_id: Optional[str] = None
    url_reference: Optional[AnyHttpUrl] = None

    def __str__(self) -> str:
        return f"{self.name}"

    @field_validator("unique_id")
    def generate_uuid(cls, v: Optional[str], info: ValidationInfo) -> str:
        values = info.data
        if v is None:
            key_values = [
                values["test_id"],
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


class ControlValidationTestForAttackTechnique(OntolocyRelationship):
    source: ControlValidationTest
    target: MitreAttackTechnique

    __relationshiptype__: ClassVar[str] = "CONTROL_VALIDATION_TEST_FOR_ATTACK_TECHNIQUE"
