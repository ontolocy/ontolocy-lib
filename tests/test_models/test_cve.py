import pytest
from pydantic import ValidationError

from ontolocy import CVE


def test_cve():
    cve = CVE(cve_id="CVE-2019-5592")

    assert cve.get_pp() == "CVE-2019-5592"


def test_cve_lower():
    cve = CVE(cve_id="cve-2019-5592")

    assert cve.get_pp() == "CVE-2019-5592"


def test_cve_bad():
    with pytest.raises(ValidationError):
        CVE(cve_id="not-2022-1234")
