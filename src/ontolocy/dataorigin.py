from typing import ClassVar, Optional
from uuid import UUID

from neontology import BaseNode, BaseRelationship
from pydantic import ValidationInfo, field_validator

from .utils import generate_deterministic_uuid


class DataOrigin(BaseNode, validate_default=True):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "DataOrigin"

    name: str
    reference: Optional[str] = None
    license: Optional[str] = None
    sharing: Optional[str] = None

    unique_id: Optional[UUID] = None

    @field_validator("unique_id")
    def generate_unique_id(cls, v: Optional[UUID], info: ValidationInfo) -> UUID:
        values = info.data
        if v is None:
            key_values = [
                values["name"],
                values["reference"],
                values["license"],
                values["sharing"],
            ]

            v = generate_deterministic_uuid(key_values)

        return v


class OriginGenerated(BaseRelationship):
    __relationshiptype__: ClassVar[Optional[str]] = "ORIGIN_GENERATED"

    source: DataOrigin
    target: BaseNode
