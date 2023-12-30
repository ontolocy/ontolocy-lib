from enum import Enum
from typing import ClassVar, Optional

from pydantic import validator

from ..node import OntolocyNode

actor_type_taxonomy = {
    "nation-state": {
        "name": "Nation State",
        "description": "An actor backed by a nation state, to achieve aims aligned with state objectives.",
    },
    "criminal-group": {
        "name": "Criminal Group",
        "description": "A group of criminals working together to conduct illegal cyber activities.",
    },
}


class ActorTypeEnum(str, Enum):
    nation_state = "nation-state"
    criminal_group = "criminal-group"


class ActorType(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "ActorType"

    unique_id: ActorTypeEnum
    name: Optional[str] = None
    description: Optional[str] = None

    @validator("name", always=True)
    def set_actor_name(cls, v, values):
        if v is None and "unique_id" in values:
            return actor_type_taxonomy[values["unique_id"]]["name"]
        else:
            return v

    @validator("description", always=True)
    def set_actor_description(cls, v, values):
        if v is None and "unique_id" in values:
            return actor_type_taxonomy[values["unique_id"]]["description"]
        else:
            return v
