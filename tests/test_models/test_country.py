import pytest
from pydantic import ValidationError

from ontolocy.models.country import Country


def test_define_country():
    my_country = Country(country_code="DE")

    assert my_country.country_code == "DE"
    assert my_country.name == "Germany"


def test_define_country_bad_code():
    with pytest.raises(ValidationError):
        Country(country_code="XX")
