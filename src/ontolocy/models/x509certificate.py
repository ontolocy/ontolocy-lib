from typing import ClassVar, Optional

from ..node import OntolocyNode


class X509Certificate(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "sha1"
    __primarylabel__: ClassVar[str] = "X509Certificate"

    sha1: str
    sha256: Optional[str] = None
    md5: Optional[str] = None

    serial_number: Optional[str] = None

    issuer_country: Optional[str] = None
    issuer_cn: Optional[str] = None
    issuer_organisation: Optional[str] = None
    issuer_locality: Optional[str] = None
    issuer_state: Optional[str] = None
    issuer_ou: Optional[str] = None

    subject_country: Optional[str] = None
    subject_cn: Optional[str] = None
    subject_organisation: Optional[str] = None
    subject_locality: Optional[str] = None
    subject_state: Optional[str] = None
    subject_ou: Optional[str] = None
