from datetime import datetime
from typing import ClassVar, Optional

from pydantic import constr

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .cpe import CPE
from .cwe import CWE


class CVE(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "cve_id"
    __primarylabel__: ClassVar[Optional[str]] = "CVE"

    cve_id: constr(to_upper=True, regex=r"CVE-\d{4}-\d{4,8}")  # noqa: F722
    published_date: Optional[datetime]
    assigner: Optional[str]


#
# OUTGOING RELATIONSHIPS
#


class CVERelatesToCWE(OntolocyRelationship):
    source: CVE
    target: CWE

    __relationshiptype__: ClassVar[str] = "CVE_RELATES_TO_CWE"


class CVERelatesToCPE(OntolocyRelationship):
    source: CVE
    target: CPE

    __relationshiptype__: ClassVar[str] = "CVE_RELATES_TO_CPE"
