from typing import ClassVar

from pydantic import AnyUrl

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship


class URLNode(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "url"
    __primarylabel__: ClassVar[str] = "URL"

    url: AnyUrl


class UrlRedirectsToUrl(OntolocyRelationship):

    __relationshiptype__: ClassVar[str] = "URL_REDIRECTS_TO_URL"

    source: URLNode
    target: URLNode
