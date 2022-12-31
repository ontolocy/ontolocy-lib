import hashlib
from typing import ClassVar, Optional

from pydantic import validator

from ..node import OntolocyNode


class Banner(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "sha1"
    __primarylabel__: ClassVar[str] = "Banner"

    banner: str
    sha1: Optional[str] = None

    @validator("sha1", always=True)
    def set_sha1(cls, v, values):
        if v is None and "banner" in values:
            return hashlib.sha1(values["banner"].encode()).hexdigest()
        else:
            return v
