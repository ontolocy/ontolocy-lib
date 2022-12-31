from typing import ClassVar, Optional

from pydantic import HttpUrl

from ..node import OntolocyNode


class CyberHarm(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "CyberHarm"

    name: str
    unique_id: str
    harm_type: str
    url_reference: HttpUrl
    description: Optional[str]
