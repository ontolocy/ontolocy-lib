from datetime import datetime
from typing import ClassVar, Optional

from pydantic import StringConstraints
from typing_extensions import Annotated

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .cpe import CPE
from .cwe import CWE


class CVE(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "cve_id"
    __primarylabel__: ClassVar[Optional[str]] = "CVE"

    cve_id: Annotated[
        str, StringConstraints(to_upper=True, pattern=r"(CVE|cve)-\d{4}-\d{4,8}")
    ]  # noqa: F722
    published_date: Optional[datetime] = None
    assigner: Optional[str] = None
    description: Optional[str] = None


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
    ] = None

    __relationshiptype__: ClassVar[str] = "CVE_RELATES_TO_CPE"
