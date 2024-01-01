from typing import ClassVar, Optional

from pydantic import ValidationInfo, field_validator

from ..node import OntolocyNode


class JarmHash(OntolocyNode):
    __primaryproperty__: ClassVar[str] = "jarm"
    __primarylabel__: ClassVar[str] = "JarmHash"

    jarm: str
    cipher_and_tls_version: Optional[str] = None
    tls_extensions_hash: Optional[str] = None

    @field_validator("cipher_and_tls_version")
    def set_cipher_and_tls_version(cls, v, info: ValidationInfo):
        """The first 30 characters of a jarm hash represent
        the cipher and tls version negotiated.
        https://engineering.salesforce.com/easily-identify-malicious-servers-on-the-internet-with-jarm-e095edac525a/
        """
        values = info.data

        if v is None and "jarm" in values:
            return values["jarm"][:30]
        else:
            return v

    @field_validator("tls_extensions_hash")
    def set_tls_extensions_hash(cls, v, info: ValidationInfo):
        """The last 32 characters of a jarm hash are a truncated sha256 hash
        of the tls extensions sent by the server.
        https://engineering.salesforce.com/easily-identify-malicious-servers-on-the-internet-with-jarm-e095edac525a/
        """
        values = info.data
        if v is None and "jarm" in values:
            return values["jarm"][-32:]
        else:
            return v
