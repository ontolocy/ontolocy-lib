import hashlib
from typing import ClassVar, Optional

from pydantic import ValidationInfo, field_validator

from ..node import OntolocyNode


class Banner(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "sha1"
    __primarylabel__: ClassVar[str] = "Banner"

    banner: str
    sha1: Optional[str] = None

    @field_validator("sha1")
    def set_sha1(cls, v, info: ValidationInfo):
        values = info.data
        if v is None and "banner" in values:
            return hashlib.sha1(values["banner"].encode()).hexdigest()
        else:
            return v
