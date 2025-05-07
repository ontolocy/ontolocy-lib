import pytest
from click.testing import CliRunner

from ontolocy.cli import cli
from ontolocy.models.actortype import actor_type_taxonomy
from ontolocy.models.country import country_codes
from ontolocy.models.sector import sectors


@pytest.mark.parametrize("prompt_input", ["\n", "no\n"])
@pytest.mark.webtest
def test_mitre_attack_no_populate(prompt_input, use_graph):
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "parse",
            "mitre-attack",
            "--url",
            "https://github.com/mitre-attack/attack-stix-data/raw/refs/heads/master/enterprise-attack/enterprise-attack-16.1.json",
        ],
        input=prompt_input,
    )

    assert (
        "Action will create up to 1763 new nodes and 21559 new relationships."
        in result.output
    )

    assert "This might take a few minutes!" in result.output

    assert "Goodbye" in result.output

    cypher = """
    MATCH (n)
    RETURN COUNT(DISTINCT n)
    """

    assert use_graph.evaluate_query_single(cypher) == 0


@pytest.mark.webtest
def test_mitre_attack_bad_prompt():
    runner = CliRunner()

    result = runner.invoke(cli, ["parse", "mitre-attack"], input="bad command\n")

    assert "Error: invalid input" in result.output


@pytest.mark.slow
@pytest.mark.webtest
def test_mitre_attack_populate_url(use_graph):
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "parse",
            "mitre-attack",
            "-u",
            "https://github.com/mitre-attack/attack-stix-data/raw/master/enterprise-attack/enterprise-attack-14.1.json",
        ],
        input="y\n",
    )

    assert "populating the graph..." in result.output
    assert "ingest complete" in result.output

    technique_cypher = """
    MATCH (n:MitreAttackTechnique)
        WHERE  (n.stix_revoked = false OR n.stix_revoked is NULL)
        AND (n.attack_deprecated = false or n.attack_deprecated is NULL)
    RETURN COUNT(DISTINCT n)
    """

    assert use_graph.evaluate_query_single(technique_cypher) == 625


def test_populate_all(use_graph):
    runner = CliRunner()

    result = runner.invoke(cli, ["populate", "all"])

    assert result.exit_code == 0
    assert "Populating all..." in result.output

    country_cypher = """MATCH (c:Country) RETURN COUNT(DISTINCT c)"""

    assert use_graph.evaluate_query_single(country_cypher) == len(country_codes.keys())

    sector_cypher = """MATCH (s:Sector) RETURN COUNT(DISTINCT s)"""

    assert use_graph.evaluate_query_single(sector_cypher) == len(sectors.keys())

    actor_type_cypher = """MATCH (a:ActorType) RETURN COUNT(DISTINCT a)"""

    assert use_graph.evaluate_query_single(actor_type_cypher) == len(
        actor_type_taxonomy.keys()
    )


def test_ingest_file(use_graph, tmp_path):
    tmp_file = tmp_path / "test.report.md"

    report_content = """---
LABEL: Report
BODY_PROPERTY: summary
title: "Example Report"
author: "Example Author"
unique_id: example-report-123
published_date: 2022-02-22
url_reference: https://example.com/
---

Example report content.

"""
    with open(tmp_file, "w") as file:
        file.write(report_content)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "import",
            str(tmp_file),
            "md",
        ],
    )

    assert result.exit_code == 0
    assert f"Importing data from {str(tmp_file)}" in result.output
