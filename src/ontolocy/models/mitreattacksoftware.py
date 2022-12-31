from datetime import datetime
from typing import ClassVar, Optional

from pydantic import HttpUrl, validator

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .mitreattacktechnique import MitreAttackTechnique


class MitreAttackSoftware(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "stix_id"
    __primarylabel__: ClassVar[str] = "MitreAttackSoftware"

    stix_id: str
    stix_type: str
    stix_created: datetime
    stix_modified: datetime
    stix_spec_version: str = "2.1"
    stix_revoked: Optional[bool] = False

    attack_spec_version: str
    attack_version: str
    attack_id: str

    ref_url: HttpUrl
    name: str
    description: Optional[str] = None

    @validator("stix_revoked")
    def set_false(cls, v):
        if v is None:
            return False
        else:
            return v


#
# OUTGOING RELATIONSHIPS
#


class MitreSoftwareUsesTechnique(OntolocyRelationship):
    source: MitreAttackSoftware
    target: MitreAttackTechnique

    __relationshiptype__: ClassVar[str] = "MITRE_SOFTWARE_USES_TECHNIQUE"
