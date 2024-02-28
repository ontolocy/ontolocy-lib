from enum import Enum
from typing import ClassVar, Optional
from uuid import UUID, uuid4

from pydantic import ValidationInfo, field_validator

from ..node import OntolocyNode
from ..utils import generate_deterministic_uuid


class HostOSEnum(str, Enum):
    linux = "linux"
    windows = "windows"
    macos = "macos"


class Host(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "Host"

    hostname: str
    os: Optional[HostOSEnum] = None
    namespace: Optional[str] = None
    unique_id: Optional[str] = None

    def __str__(self) -> str:
        return self.hostname

    @field_validator("namespace")
    def set_namespace(cls, v):
        if v is None:
            return str(uuid4())

        else:
            return v

    @field_validator("unique_id")
    def generate_instance_id(cls, v: Optional[UUID], info: ValidationInfo) -> UUID:
        values = info.data

        if v is None:
            key_values = [values["hostname"], values["namespace"]]

            v = str(generate_deterministic_uuid(key_values))

        return v
