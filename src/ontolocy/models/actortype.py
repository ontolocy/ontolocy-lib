from enum import Enum
from typing import ClassVar, Optional

from pydantic import ValidationInfo, field_validator

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
    "hacktivists": {
        "name": "Hacktivists",
        "description": "An individual or group who's cyber activities are primarily ideologically driven.",
    },
    "commercial-provider": {
        "name": "Commercial Provider",
        "description": (
            "An actor who sells offensive cyber services to others,"
            " and those services are deemed legal in the jurisdiction that they operate within."
            " Also known as 'hackers-for-hire'"
        ),
    },
}


class ActorTypeEnum(str, Enum):
    nation_state = "nation-state"
    criminal_group = "criminal-group"
    hacktivists = "hacktivists"
    commercial_provider = "commercial-provider"


class ActorType(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "ActorType"

    unique_id: ActorTypeEnum
    name: Optional[str] = None
    description: Optional[str] = None

    def __str__(self) -> str:
        if self.name is not None:
            return self.name
        else:
            return self.unique_id

    @field_validator("name")
    def set_actor_name(cls, v, info: ValidationInfo):
        values = info.data
        if v is None and "unique_id" in values:
            return actor_type_taxonomy[values["unique_id"]]["name"]
        else:
            return v

    @field_validator("description")
    def set_actor_description(cls, v, info: ValidationInfo):
        values = info.data
        if v is None and "unique_id" in values:
            return actor_type_taxonomy[values["unique_id"]]["description"]
        else:
            return v
