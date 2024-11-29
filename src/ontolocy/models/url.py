from typing import ClassVar

from pydantic import AnyUrl, field_serializer

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship


class URLNode(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "url"
    __primarylabel__: ClassVar[str] = "URL"

    url: AnyUrl

    @field_serializer("url")
    def serialize_to_str(self, input: AnyUrl, _info):
        return str(input)


class UrlRedirectsToUrl(OntolocyRelationship):
    __relationshiptype__: ClassVar[str] = "URL_REDIRECTS_TO_URL"

    source: URLNode
    target: URLNode
