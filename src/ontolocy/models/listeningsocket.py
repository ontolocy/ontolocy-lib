from enum import Enum
from typing import Any, ClassVar, Dict, Optional
from uuid import UUID

from pydantic import IPvAnyAddress, validator

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
    ip_address_unique_id: Optional[
        UUID
    ] = None  # for private IPs, uniquely identify the IP to avoid collisions

    unique_id: Optional[UUID] = None

    @validator("unique_id", always=True)
    def generate_socket_uuid(cls, v: Optional[UUID], values: Dict[str, Any]) -> UUID:

        if v is None:

            key_values = [
                values["protocol"],
                values["port_number"],
                values["ip_address"],
                values["ip_address_unique_id"],
            ]

            v = generate_deterministic_uuid(key_values)

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
    status_code: Optional[int]

    __relationshiptype__: ClassVar[str] = "SERVICE_HOSTS_URL"


class ServiceIdentifiedAsPlatform(OntolocyRelationship):
    source: ListeningSocket
    target: CPE
    status_code: Optional[int]

    __relationshiptype__: ClassVar[str] = "SERVICE_IDENTIFIED_AS_PLATFORM"
