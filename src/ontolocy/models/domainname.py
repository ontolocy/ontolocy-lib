import re
from typing import ClassVar, Optional

from pydantic import validator

from ..node import OntolocyNode


class DomainName(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "name"
    __primarylabel__: ClassVar[Optional[str]] = "DomainName"

    name: str

    @validator("name")
    def validate_domain(cls, v: str) -> str:
        pattern = r"((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}"
        m = re.match(pattern, v)

        if m is None:
            raise ValueError("Doesn't look like a valid domain")

        return v
