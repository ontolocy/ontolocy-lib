from typing import ClassVar

from ..node import OntolocyNode


class CobaltStrikeWatermark(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "value"
    __primarylabel__: ClassVar[str] = "CobaltStrikeWatermark"

    value: int
