from typing import ClassVar, Optional

from pydantic import constr, validator

from ..node import OntolocyNode


class CPE(OntolocyNode):
    """Defines the CPE (common platform enumeration) node type

    We only look at the part, vendor and product.
    We don't create a whole new node for every possible version.

    We take a 2.3 or 2.2 string and convert it to a 2.3 string
        without version/update/edition information.
    """

    __primaryproperty__: ClassVar[str] = "cpe"
    __primarylabel__: ClassVar[Optional[str]] = "CPE"

    cpe: constr(
        regex=(
            r"(cpe:2\.3:[aho\*\-](:(((\?*|\*?)([a-zA-Z0-9\-\._]|"  # noqa: F722
            r"(\\[\\\*\?!#$$%&'\(\)\+,/:;<=>@\[\]\^`\{\|}~]))+(\?*|\*?))|[\*\-])){5}"
            r"(:(([a-zA-Z]{2,3}(-([a-zA-Z]{2}|[0-9]{3}))?)|[\*\-]))(:(((\?*|\*?)"
            r"([a-zA-Z0-9\-\._]|(\\[\\\*\?!#$$%&'\(\)\+,/:;<=>@\[\]\^`\{\|}~]))+(\?*|\*?))|[\*\-])){4})"
        )
    )
    cpe_version: str = "2.3"
    part: str = None
    vendor: str = None
    product: str = None

    @validator("cpe", always=True, pre=True)
    def set_cpe(cls, v):

        # hack to handle CPEs with colons in (which will be escaped with a backslash)
        v = v.replace(r"\:", r"\;")

        cpe_parts = v.split(":")

        if cpe_parts[0] != "cpe":
            raise ValueError("Doesn't look like a valid CPE")

        if cpe_parts[1] == "2.3":
            v = f"cpe:{cpe_parts[1]}:{cpe_parts[2]}:{cpe_parts[3]}:{cpe_parts[4]}:*:*:*:*:*:*:*:*"

        # here's where we attempt to convert 2.2 format to 2.3
        elif cpe_parts[1] == "/a":
            v = f"cpe:2.3:a:{cpe_parts[2]}:{cpe_parts[3]}:*:*:*:*:*:*:*:*"

        elif cpe_parts[1] == "/o":
            v = f"cpe:2.3:o:{cpe_parts[2]}:{cpe_parts[3]}:*:*:*:*:*:*:*:*"

        elif cpe_parts[1] == "/h":
            v = f"cpe:2.3:h:{cpe_parts[2]}:{cpe_parts[3]}:*:*:*:*:*:*:*:*"

        else:
            raise ValueError("Doesn't look like a valid CPE")

        v = v.replace(r"\;", r"\:")

        return v

    @validator("part", always=True)
    def set_part(cls, v, values):
        if v is None and "cpe" in values:
            cpe_parts = values["cpe"].split(":")
            if cpe_parts[2] in ["a", "h", "o"]:
                return cpe_parts[2]
            else:
                raise ValueError("Doesn't look like a valid CPE part (a/h/o)")
        else:
            return v

    @validator("vendor", always=True)
    def set_vendor(cls, v, values):
        if v is None and "cpe" in values:
            cpe_parts = values["cpe"].split(":")
            return cpe_parts[3]
        else:
            return v

    @validator("product", always=True)
    def set_product(cls, v, values):
        if v is None and "cpe" in values:
            cpe_parts = values["cpe"].split(":")
            return cpe_parts[4]
        else:
            return v
