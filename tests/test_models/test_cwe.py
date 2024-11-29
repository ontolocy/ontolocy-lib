from ontolocy import CWE


def test_cwe():
    cwe = CWE(
        cwe_id=1001,
        description="hello world",
        name="foo bar",
        abstraction="Something",
        structure="something else",
        status="active",
    )

    assert cwe.get_pp() == 1001


def test_cwe_letters():
    cwe = CWE(
        cwe_id="1001",
        description="hello world",
        name="foo bar",
        abstraction="Something",
        structure="something else",
        status="active",
    )

    assert cwe.get_pp() == 1001
