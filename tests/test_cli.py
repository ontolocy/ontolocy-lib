from click.testing import CliRunner
from ontolocy.cli import cli

import pytest


@pytest.mark.parametrize("prompt_input", ["\n", "no\n"])
@pytest.mark.webtest
def test_mitre_attack_no_populate(prompt_input):

    runner = CliRunner()

    result = runner.invoke(cli, ["parse", "mitre-attack"], input=prompt_input)

    print(result.output)

    assert (
        "Action will create up to 2047 new nodes and 19695 new relationships."
        in result.output
    )

    assert "This might take a few minutes!" in result.output

    assert "Goodbye" in result.output


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
