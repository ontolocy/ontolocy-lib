import pytest
import requests

from ontolocy.tools import MitreAttackParser

test_cases = [
    {
        "version": "14.1",
        "url": "https://github.com/mitre-attack/attack-stix-data/raw/master/enterprise-attack/enterprise-attack-14.1.json",
        "campaign_count": 23,
        "software_count": 649,
        "tactic_count": 14,
        "technique_count": 625,
        "data_source_count": 37,
        "data_component_count": 106,
        "mitigation_count": 43,
        "group_count": 142,
        "campaign_count_valid": 23,
        "software_count_valid": 649,
        "tactic_count_valid": 14,
        "technique_count_valid": 625,
        "data_source_count_valid": 37,
        "data_component_count_valid": 106,
        "mitigation_count_valid": 43,
        "group_count_valid": 142,
    }
]


@pytest.mark.webtest
@pytest.mark.parametrize("test_data", test_cases)
def test_detect(test_data):
    parser = MitreAttackParser()

    response = requests.get(test_data["url"])
    input_data = str(response.text)

    assert parser.detect(input_data) is True


def test_detect_bad():
    parser = MitreAttackParser()

    assert parser.detect("just some text") is False


@pytest.mark.webtest
@pytest.mark.parametrize("test_data", test_cases)
def test_node_parse(test_data):
    parser = MitreAttackParser()

    parser.parse_url(test_data["url"], populate=False)

    node_df = parser.node_oriented_dfs["MitreAttackCampaign"]

    assert len(node_df.index) == test_data["campaign_count"]

    software_df = parser.node_oriented_dfs["MitreAttackSoftware"]

    assert len(software_df.index) == test_data["software_count"]

    tactic_df = parser.node_oriented_dfs["MitreAttackTactic"]

    assert len(tactic_df.index) == test_data["tactic_count"]

    technique_df = parser.node_oriented_dfs["MitreAttackTechnique"]

    assert len(technique_df.index) == test_data["technique_count"]

    ds_df = parser.node_oriented_dfs["MitreAttackDataSource"]

    assert len(ds_df.index) == test_data["data_source_count"]

    dc_df = parser.node_oriented_dfs["MitreAttackDataComponent"]

    assert len(dc_df.index) == test_data["data_component_count"]

    mitigation_df = parser.node_oriented_dfs["MitreAttackMitigation"]

    assert len(mitigation_df.index) == test_data["mitigation_count"]

    group_df = parser.node_oriented_dfs["MitreAttackGroup"]

    assert len(group_df.index) == test_data["group_count"]


@pytest.mark.slow
@pytest.mark.webtest
@pytest.mark.parametrize("test_data", test_cases)
def test_node_populate_simple(use_graph, test_data):
    parser = MitreAttackParser()

    parser.parse_url(test_data["url"], populate=True)

    campaign_cypher = """
    MATCH (n:MitreAttackCampaign)
        WHERE  (n.stix_revoked = false OR n.stix_revoked is NULL)
        AND (n.attack_deprecated = false or n.attack_deprecated is NULL)
    RETURN COUNT(DISTINCT n)
    """

    assert (
        use_graph.evaluate_query_single(campaign_cypher)
        == test_data["campaign_count_valid"]
    )


@pytest.mark.slow
@pytest.mark.webtest
@pytest.mark.parametrize("test_data", test_cases)
def test_node_populate(use_graph, test_data):
    parser = MitreAttackParser()

    parser.parse_url(test_data["url"], populate=True)

    campaign_cypher = """
    MATCH (n:MitreAttackCampaign)
        WHERE  (n.stix_revoked = false OR n.stix_revoked is NULL)
        AND (n.attack_deprecated = false or n.attack_deprecated is NULL)
    RETURN COUNT(DISTINCT n)
    """

    assert (
        use_graph.evaluate_query_single(campaign_cypher)
        == test_data["campaign_count_valid"]
    )

    software_cypher = """
    MATCH (n:MitreAttackSoftware)
        WHERE  (n.stix_revoked = false OR n.stix_revoked is NULL)
        AND (n.attack_deprecated = false or n.attack_deprecated is NULL)
    RETURN COUNT(DISTINCT n)
    """

    assert (
        use_graph.evaluate_query_single(software_cypher)
        == test_data["software_count_valid"]
    )

    tactic_cypher = """
    MATCH (n:MitreAttackTactic)
        WHERE  (n.stix_revoked = false OR n.stix_revoked is NULL)
        AND (n.attack_deprecated = false or n.attack_deprecated is NULL)
    RETURN COUNT(DISTINCT n)
    """

    assert (
        use_graph.evaluate_query_single(tactic_cypher)
        == test_data["tactic_count_valid"]
    )

    technique_cypher = """
    MATCH (n:MitreAttackTechnique)
        WHERE  (n.stix_revoked = false OR n.stix_revoked is NULL)
        AND (n.attack_deprecated = false or n.attack_deprecated is NULL)
    RETURN COUNT(DISTINCT n)
    """

    assert (
        use_graph.evaluate_query_single(technique_cypher)
        == test_data["technique_count_valid"]
    )

    ds_cypher = """
    MATCH (n:MitreAttackDataSource)
        WHERE  (n.stix_revoked = false OR n.stix_revoked is NULL)
        AND (n.attack_deprecated = false or n.attack_deprecated is NULL)
    RETURN COUNT(DISTINCT n)
    """
    assert (
        use_graph.evaluate_query_single(ds_cypher)
        == test_data["data_source_count_valid"]
    )

    dc_cypher = """
    MATCH (n:MitreAttackDataComponent)
        WHERE  (n.stix_revoked = false OR n.stix_revoked is NULL)
        AND (n.attack_deprecated = false or n.attack_deprecated is NULL)
    RETURN COUNT(DISTINCT n)
    """

    assert (
        use_graph.evaluate_query_single(dc_cypher)
        == test_data["data_component_count_valid"]
    )

    mitigation_cypher = """
    MATCH (mitigation:MitreAttackMitigation)
        WHERE  (mitigation.stix_revoked = false OR mitigation.stix_revoked is NULL)
            AND (mitigation.attack_deprecated = false or mitigation.attack_deprecated is NULL)
    RETURN COUNT(DISTINCT mitigation)
    """

    assert (
        use_graph.evaluate_query_single(mitigation_cypher)
        == test_data["mitigation_count_valid"]
    )

    group_cypher = """
    MATCH (n:MitreAttackGroup)
        WHERE  (n.stix_revoked = false OR n.stix_revoked is NULL)
        AND (n.attack_deprecated = false or n.attack_deprecated is NULL)
    RETURN COUNT(DISTINCT n)
    """

    assert (
        use_graph.evaluate_query_single(group_cypher) == test_data["group_count_valid"]
    )
