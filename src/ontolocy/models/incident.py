from datetime import date
from typing import ClassVar, List, Optional

from pydantic import HttpUrl, field_serializer

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .intrusionset import IntrusionSet
from .report import Report
from .sector import Sector
from .threatactor import ThreatActor


class Incident(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "Incident"

    name: str
    summary: Optional[str] = None
    unique_id: str
    incident_date: date
    impact: Optional[str] = None
    cost_usd: Optional[int] = None

    url_reference: Optional[HttpUrl] = None
    additional_urls: Optional[List[HttpUrl]] = None

    def __str__(self) -> str:
        return self.name

    @field_serializer("url_reference")
    def serialize_to_str(self, input: HttpUrl, _info):
        return str(input)

    @field_serializer("additional_urls")
    def serialize_list_to_str(self, input: Optional[List[HttpUrl]], _info):
        if input:
            return [str(url) for url in input]


class IncidentReferencedByReport(OntolocyRelationship):
    source: Incident
    target: Report

    __relationshiptype__: ClassVar[str] = "INCIDENT_REFERENCED_BY_REPORT"


class IncidentLinkedToIntrusionSet(OntolocyRelationship):
    source: Incident
    target: IntrusionSet

    url_reference: Optional[HttpUrl] = None

    __relationshiptype__: ClassVar[str] = "INCIDENT_LINKED_TO_INTRUSION_SET"

    @field_serializer("url_reference")
    def serialize_to_str(self, input: HttpUrl, _info):
        return str(input)


class IncidentLinkedToThreatActor(OntolocyRelationship):
    source: Incident
    target: ThreatActor

    url_reference: Optional[HttpUrl] = None

    __relationshiptype__: ClassVar[str] = "INCIDENT_LINKED_TO_THREAT_ACTOR"

    @field_serializer("url_reference")
    def serialize_to_str(self, input: HttpUrl, _info):
        return str(input)


class IncidentAffectedSector(OntolocyRelationship):
    source: Incident
    target: Sector

    url_reference: Optional[HttpUrl] = None

    __relationshiptype__: ClassVar[str] = "INCIDENT_AFFECTED_SECTOR"

    @field_serializer("url_reference")
    def serialize_to_str(self, input: HttpUrl, _info):
        return str(input)
