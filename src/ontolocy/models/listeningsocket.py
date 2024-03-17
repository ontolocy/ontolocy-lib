from enum import Enum
from ipaddress import ip_address
from typing import ClassVar, Optional
from uuid import uuid4

from pydantic import IPvAnyAddress, StringConstraints, ValidationInfo, field_validator
from typing_extensions import Annotated

from ontolocy.models.port import Port
from ontolocy.node import OntolocyNode
from ontolocy.relationship import OntolocyRelationship
from ontolocy.utils import generate_deterministic_uuid

from .banner import Banner
from .cpe import CPE
from .jarmhash import JarmHash
from .url import URLNode
from .x509certificate import X509Certificate


class ListeningSocketProtocolEnum(str, Enum):
    tcp = "tcp"
    udp = "udp"
    sctp = "sctp"


class ListeningSocket(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "ListeningSocket"

    protocol: ListeningSocketProtocolEnum
    port_number: int
    ip_address: IPvAnyAddress
    private: Optional[bool] = None
    namespace: Optional[str] = None
    ip_address_unique_id: Optional[str] = (
        None  # for private IPs, uniquely identify the IP to avoid collisions
    )

    unique_id: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.ip_address}:{self.port_number} ({self.protocol.value})"

    @field_validator("unique_id")
    def generate_socket_uuid(cls, v: Optional[str], info: ValidationInfo) -> str:
        values = info.data
        if v is None:
            key_values = [
                values["protocol"],
                values["port_number"],
                values["ip_address"],
                values["ip_address_unique_id"],
            ]

            v = str(generate_deterministic_uuid(key_values))

        return v

    @field_validator("private")
    def mark_private(cls, v, info: ValidationInfo):
        values = info.data
        if v is None and "ip_address" in values:
            return ip_address(values["ip_address"]).is_private
        else:
            return v

    @field_validator("namespace")
    def set_namespace(cls, v, info: ValidationInfo):
        values = info.data

        if values["private"] is False:
            return None

        elif v is None:
            return str(uuid4())

        else:
            return v

    @field_validator("ip_address_unique_id")
    def generate_ip_id(cls, v: Optional[str], info: ValidationInfo) -> str:
        values = info.data
        if v is None and values["private"] and values.get("namespace"):
            key_values = [values["ip_address"], values["namespace"]]

            v = str(generate_deterministic_uuid(key_values))

        elif v is None:
            v = str(values["ip_address"])

        return v


#
# OUTGOING RELATIONSHIPS
#


class ListeningSocketUsesPort(OntolocyRelationship):
    source: ListeningSocket
    target: Port

    __relationshiptype__: ClassVar[str] = "LISTENING_SOCKET_USES_PORT"


class OpenPortPresentsBanner(OntolocyRelationship):
    source: ListeningSocket
    target: Banner

    __relationshiptype__: ClassVar[str] = "OPEN_PORT_PRESENTS_BANNER"


class OpenPortPresentsX509Certificate(OntolocyRelationship):
    source: ListeningSocket
    target: X509Certificate

    __relationshiptype__: ClassVar[str] = "OPEN_PORT_PRESENTS_X509_CERTIFICATE"


class OpenPortHasJarmHash(OntolocyRelationship):
    source: ListeningSocket
    target: JarmHash

    __relationshiptype__: ClassVar[str] = "OPEN_PORT_HAS_JARM_HASH"


class ServiceHostsURL(OntolocyRelationship):
    source: ListeningSocket
    target: URLNode
    status_code: Optional[int] = None

    __relationshiptype__: ClassVar[str] = "SERVICE_HOSTS_URL"


class ServiceIdentifiedAsPlatform(OntolocyRelationship):
    source: ListeningSocket
    target: CPE
    status_code: Optional[int] = None

    cpe: Optional[
        Annotated[
            str,
            StringConstraints(
                pattern=(
                    r"(cpe:2\.3:[aho\*\-](:(((\?*|\*?)([a-zA-Z0-9\-\._]|"  # noqa: F722
                    r"(\\[\\\*\?!#$$%&'\(\)\+,/:;<=>@\[\]\^`\{\|}~]))+(\?*|\*?))|[\*\-])){5}"
                    r"(:(([a-zA-Z]{2,3}(-([a-zA-Z]{2}|[0-9]{3}))?)|[\*\-]))(:(((\?*|\*?)"
                    r"([a-zA-Z0-9\-\._]|(\\[\\\*\?!#$$%&'\(\)\+,/:;<=>@\[\]\^`\{\|}~]))+(\?*|\*?))|[\*\-])){4})"
                )
            ),
        ]
    ]

    @field_validator("cpe", mode="before")
    def set_cpe(cls, v):
        # hack to handle CPEs with colons in (which will be escaped with a backslash)
        v = v.replace(r"\:", r"\;")

        cpe_parts = v.split(":")

        if cpe_parts[0] != "cpe":
            raise ValueError("Doesn't look like a valid CPE")

        if cpe_parts[1] == "2.3":
            v = "cpe"

            for idx in range(1, 13):
                v += ":"
                if idx < len(cpe_parts):
                    v += cpe_parts[idx]
                else:
                    v += "*"

        else:
            raise ValueError("Doesn't look like a compatible CPE 2.3 format")

        return v

    __relationshiptype__: ClassVar[str] = "SERVICE_IDENTIFIED_AS_PLATFORM"
