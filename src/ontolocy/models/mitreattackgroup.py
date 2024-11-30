from datetime import datetime
from typing import ClassVar, Optional

from pydantic import HttpUrl, field_serializer

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .mitreattacksoftware import MitreAttackSoftware
from .mitreattacktechnique import MitreAttackTechnique


class MitreAttackGroup(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "stix_id"
    __primarylabel__: ClassVar[str] = "MitreAttackGroup"

    stix_id: str
    stix_type: str
    stix_created: datetime
    stix_modified: datetime
    stix_spec_version: str = "2.1"
    stix_revoked: Optional[bool] = False

    attack_spec_version: str
    attack_version: str
    attack_id: str
    attack_deprecated: Optional[bool] = False

    ref_url: HttpUrl
    name: str
    description: Optional[str] = None

    @field_serializer("ref_url")
    def serialize_ref_url(self, ref_url: HttpUrl, _info):
        return str(ref_url)

    def __str__(self) -> str:
        return self.name


#
# OUTGOING RELATIONSHIPS
#


class MitreAttackGroupUsesTechnique(OntolocyRelationship):
    source: MitreAttackGroup
    target: MitreAttackTechnique

    __relationshiptype__: ClassVar[str] = "MITRE_ATTACK_GROUP_USES_TECHNIQUE"


class MitreAttackGroupUsesSoftware(OntolocyRelationship):
    source: MitreAttackGroup
    target: MitreAttackSoftware

    __relationshiptype__: ClassVar[str] = "MITRE_ATTACK_GROUP_USES_SOFTWARE"
