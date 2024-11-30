from datetime import datetime
from typing import ClassVar, Optional

from neontology import related_nodes, related_property
from pydantic import HttpUrl, StringConstraints, field_serializer
from typing_extensions import Annotated

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

    attack_id: Annotated[
        str, StringConstraints(to_upper=True, pattern=r"T\d{4}(?:\.\d{3})?")
    ]  # noqa: F722
    attack_spec_version: str
    attack_subtechnique: Optional[bool] = False
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

    @property
    @related_property
    def tactic_names(self):
        return "MATCH (#ThisNode)<-[:MITRE_TACTIC_INCLUDES_TECHNIQUE]-(t) RETURN COLLECT(t.name)"

    @property
    @related_nodes
    def tactic_nodes(self):
        return "MATCH (#ThisNode)<-[:MITRE_TACTIC_INCLUDES_TECHNIQUE]-(t) RETURN t"


#
# OUTGOING RELATIONSHIPS
#


class MitreSubtechniqueOf(OntolocyRelationship):
    source: MitreAttackTechnique
    target: MitreAttackTechnique

    __relationshiptype__: ClassVar[str] = "MITRE_SUBTECHNIQUE_OF"
