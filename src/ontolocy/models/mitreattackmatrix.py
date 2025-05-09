from datetime import datetime
from typing import ClassVar, Optional

from pydantic import HttpUrl, field_serializer

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .mitreattacktactic import MitreAttackTactic


class MitreAttackMatrix(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "stix_id"
    __primarylabel__: ClassVar[str] = "MitreAttackMatrix"

    stix_id: str
    stix_type: str
    stix_created: datetime
    stix_modified: datetime
    stix_spec_version: str = "2.1"
    stix_revoked: Optional[bool] = False

    attack_id: str
    attack_spec_version: str
    attack_version: str
    attack_deprecated: Optional[bool] = False

    ref_url: HttpUrl
    name: str
    description: str

    @field_serializer("ref_url")
    def serialize_ref_url(self, ref_url: HttpUrl, _info):
        return str(ref_url)

    def __str__(self) -> str:
        return f"{self.attack_id}: {self.name}"


#
# OUTGOING RELATIONSHIPS
#


class MitreMatrixIncludesTactic(OntolocyRelationship):
    source: MitreAttackMatrix
    target: MitreAttackTactic

    __relationshiptype__: ClassVar[str] = "MITRE_MATRIX_INCLUDES_TACTIC"
