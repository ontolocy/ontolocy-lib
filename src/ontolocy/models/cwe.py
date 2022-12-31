from typing import ClassVar, Optional

from ..node import OntolocyNode


class CWE(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "cwe_id"
    __primarylabel__: ClassVar[Optional[str]] = "CWE"

    cwe_id: int
    description: str
    name: str
    abstraction: str
    structure: str
    status: str
