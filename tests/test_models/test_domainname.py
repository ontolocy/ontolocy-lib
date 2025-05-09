import pytest
from pydantic import ValidationError

from ontolocy.models.domainname import DomainName


def test_domainname():
    domain = DomainName(name="example.com")

    assert domain.name == "example.com"


def test_domainname_badname():
    with pytest.raises(ValidationError):
        DomainName(name="notadomain")
