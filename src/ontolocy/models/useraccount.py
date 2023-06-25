from typing import Any, ClassVar, Dict, Optional
from uuid import UUID, uuid4

from pydantic import validator

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from ..utils import generate_deterministic_uuid
from .host import Host


class UserAccount(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "UserAccount"

    username: str
    local_hostname: Optional[str]
    namespace: Optional[str] = None
    unique_id: Optional[UUID] = None

    def get_identifier(self) -> str:
        return self.username

    @validator("namespace", always=True)
    def set_namespace(cls, v, values: Dict[str, Any]) -> str:

        if v is None:
            return str(uuid4())

        else:
            return v

    @validator("unique_id", always=True)
    def generate_instance_id(cls, v: Optional[UUID], values: Dict[str, Any]) -> UUID:

        if v is None:

            key_values = [
                values["username"],
                values["local_hostname"],
                values["namespace"],
            ]

            v = generate_deterministic_uuid(key_values)

        return v


class UserAccountAuthorizedOnHost(OntolocyRelationship):

    __relationshiptype__: ClassVar[str] = "USER_ACCOUNT_AUTHORIZED_ON_HOST"

    source: UserAccount
    target: Host
