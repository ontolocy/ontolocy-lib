from datetime import datetime
from typing import ClassVar, Optional

from pydantic import HttpUrl, constr, validator

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .mitreattacktechnique import MitreAttackTechnique


class MitreAttackTactic(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "stix_id"
    __primarylabel__: ClassVar[str] = "MitreAttackTactic"

    stix_id: str
    stix_type: str
    stix_created: datetime
    stix_modified: datetime
    stix_spec_version: str = "2.1"
    stix_revoked: Optional[bool] = False

    attack_id: constr(to_upper=True, regex=r"TA\d{4}")  # noqa: F722
    attack_spec_version: str
    attack_version: str
    attack_shortname: str

    ref_url: HttpUrl
    name: str
    description: str

    @validator("stix_revoked")
    def set_false(cls, v):
        if v is None:
            return False
        else:
            return v


#
# OUTGOING RELATIONSHIPS
#


class MitreTacticIncludesTechnique(OntolocyRelationship):
    source: MitreAttackTactic
    target: MitreAttackTechnique

    __relationshiptype__: ClassVar[str] = "MITRE_TACTIC_INCLUDES_TECHNIQUE"
