from typing import ClassVar, Optional

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .port import Port


class NetworkService(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "name"
    __primarylabel__: ClassVar[Optional[str]] = "NetworkService"

    name: str
    description: Optional[str] = None


#
# OUTGOING RELATIONSHIPS
#


class NetworkServiceRunsOnPort(OntolocyRelationship):
    source: NetworkService
    target: Port

    __relationshiptype__: ClassVar[str] = "NETWORK_SERVICE_RUNS_ON_PORT"
