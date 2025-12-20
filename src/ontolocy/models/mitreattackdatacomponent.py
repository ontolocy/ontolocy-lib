from datetime import datetime
from typing import ClassVar, Optional

from pydantic import HttpUrl, field_serializer

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .mitreattacktechnique import MitreAttackTechnique


class MitreAttackDataComponent(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "stix_id"
    __primarylabel__: ClassVar[str] = "MitreAttackDataComponent"

    stix_id: str
    stix_type: str
    stix_created: datetime
    stix_modified: datetime
    stix_spec_version: str = "2.1"
    stix_revoked: Optional[bool] = False

    attack_spec_version: str
    attack_version: str
    attack_deprecated: Optional[bool] = False

    name: str
    description: str

    attack_id: Optional[str] = None
    ref_url: Optional[HttpUrl] = None

    @field_serializer("ref_url")
    def serialize_ref_url(self, ref_url: Optional[HttpUrl], _info):
        if ref_url is None:
            return None
        else:
            return str(ref_url)


#
# OUTGOING RELATIONSHIPS
#


class MitreAttackDataComponentDetectsTechnique(OntolocyRelationship):
    source: MitreAttackDataComponent
    target: MitreAttackTechnique

    __relationshiptype__: ClassVar[str] = (
        "MITRE_ATTACK_DATA_COMPONENT_DETECTS_TECHNIQUE"
    )
