from typing import ClassVar, Optional, Dict, Any
from uuid import UUID, uuid4

from pydantic import validator

from ..node import OntolocyNode
from ..utils import generate_deterministic_uuid


class Host(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "Host"

    hostname: str
    namespace: Optional[str] = None
    unique_id: Optional[UUID] = None

    def get_identifier(self) -> str:
        return self.hostname

    @validator("namespace", always=True)
    def set_namespace(cls, v, values: Dict[str, Any]):

        if v is None:
            return str(uuid4())

        else:
            return v

    @validator("unique_id", always=True)
    def generate_instance_id(cls, v: Optional[UUID], values: Dict[str, Any]) -> UUID:

        if v is None:

            key_values = [values["hostname"], values["namespace"]]

            v = generate_deterministic_uuid(key_values)

        return v
