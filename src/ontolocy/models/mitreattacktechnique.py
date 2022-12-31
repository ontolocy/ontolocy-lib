from datetime import datetime
from typing import ClassVar, Optional

from pydantic import HttpUrl, constr, validator

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship


class MitreAttackTechnique(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "stix_id"
    __primarylabel__: ClassVar[str] = "MitreAttackTechnique"

    stix_id: str
    stix_type: str
    stix_created: datetime
    stix_modified: datetime
    stix_spec_version: str = "2.1"
    stix_revoked: Optional[bool] = False

    attack_id: constr(to_upper=True, regex=r"T\d{4}(?:\.\d{3})?")  # noqa: F722
    attack_spec_version: str
    attack_subtechnique: Optional[bool] = False
    attack_version: str

    ref_url: HttpUrl
    name: str
    description: str

    @validator("stix_revoked", "attack_subtechnique")
    def set_false(cls, v):
        if v is None:
            return False
        else:
            return v


#
# OUTGOING RELATIONSHIPS
#


class MitreSubtechniqueOf(OntolocyRelationship):
    source: MitreAttackTechnique
    target: MitreAttackTechnique

    __relationshiptype__: ClassVar[str] = "MITRE_SUBTECHNIQUE_OF"
