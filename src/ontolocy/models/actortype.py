from typing import ClassVar, Optional

from pydantic import HttpUrl

from ..node import OntolocyNode


class ActorType(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "ActorType"

    name: str
    unique_id: str
    url_reference: HttpUrl
    description: Optional[str]
