import pytest
import requests

from ontolocy.tools import CapecParser

test_cases = [
    {"url": "https://capec.mitre.org/data/xml/capec_v3.9.xml", "attack_patterns": 559}
]


@pytest.mark.webtest
@pytest.mark.parametrize("test_data", test_cases)
def test_detect(test_data):
    parser = CapecParser()

    response = requests.get(test_data["url"])
    input_data = parser._load_data(response.text)

    assert parser.detect(input_data) is True


def test_detect_bad():
    parser = CapecParser()

    assert parser.detect("just some text") is False


@pytest.mark.webtest
@pytest.mark.parametrize("test_data", test_cases)
def test_node_parse(test_data):
    parser = CapecParser()

    parser.parse_url(test_data["url"], populate=False)

    capec_pattern_df = parser.node_oriented_dfs["CAPECPattern"]

    assert (
        len(capec_pattern_df[capec_pattern_df["status"] != "Deprecated"].index)
        == test_data["attack_patterns"]
    )


@pytest.mark.slow
@pytest.mark.webtest
@pytest.mark.parametrize("test_data", test_cases)
def test_populate(use_graph, test_data):
    parser = CapecParser()

    parser.parse_url(test_data["url"], populate=True)

    cypher = """MATCH (n:CAPECPattern) WHERE n.status <> 'Deprecated' RETURN COUNT(DISTINCT n)"""

    result = use_graph.evaluate_query_single(cypher)

    assert result == test_data["attack_patterns"]
