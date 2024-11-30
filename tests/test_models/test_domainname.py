from ontolocy.models.domainname import DomainName

from pydantic import ValidationError
import pytest


def test_domainname():
    domain = DomainName(name="example.com")

    assert domain.name == "example.com"


def test_domainname_badname():
    with pytest.raises(ValidationError):
        DomainName(name="notadomain")
