from typing import ClassVar, Optional
from uuid import UUID, uuid4

from pydantic import ValidationInfo, field_validator

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from ..utils import generate_deterministic_uuid
from .host import Host


class UserAccount(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "UserAccount"

    username: str
    local_hostname: Optional[str] = None
    namespace: Optional[str] = None
    unique_id: Optional[UUID] = None

    def __str__(self) -> str:
        return self.username

    @field_validator("namespace")
    def set_namespace(cls, v) -> str:
        if v is None:
            return str(uuid4())

        else:
            return v

    @field_validator("unique_id")
    def generate_instance_id(cls, v: Optional[UUID], info: ValidationInfo) -> UUID:
        values = info.data

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
