from ontolocy.cli import cli
from ontolocy.tools import NVDCVEEnricher, NVDCVEParser
from ontolocy.tools.nvd import NVDCVEOntolocyClient

test_data = {
    "resultsPerPage": 1,
    "startIndex": 0,
    "totalResults": 1,
    "format": "NVD_CVE",
    "version": "2.0",
    "timestamp": "2025-05-05T16:22:48.334",
    "vulnerabilities": [
        {
            "cve": {
                "id": "CVE-2019-1010218",
                "sourceIdentifier": "josh@bress.net",
                "published": "2019-07-22T18:15:10.917",
                "lastModified": "2024-11-21T04:18:03.857",
                "vulnStatus": "Modified",
                "cveTags": [],
                "descriptions": [
                    {
                        "lang": "en",
                        "value": "Cherokee Webserver Latest Cherokee Web server Upto Version 1.2.103 (Current stable) is affected by: Buffer Overflow - CWE-120. The impact is: Crash. The component is: Main cherokee command. The attack vector is: Overwrite argv[0] to an insane length with execl. The fixed version is: There's no fix yet.",
                    },
                    {
                        "lang": "es",
                        "value": "El servidor web de Cherokee más reciente de Cherokee Webserver Hasta Versión 1.2.103 (estable actual) está afectado por: Desbordamiento de Búfer - CWE-120. El impacto es: Bloqueo. El componente es: Comando cherokee principal. El vector de ataque es: Sobrescribir argv[0] en una longitud no sana con execl. La versión corregida es: no hay ninguna solución aún.",
                    },
                ],
                "metrics": {
                    "cvssMetricV31": [
                        {
                            "source": "nvd@nist.gov",
                            "type": "Primary",
                            "cvssData": {
                                "version": "3.1",
                                "vectorString": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H",
                                "baseScore": 7.5,
                                "baseSeverity": "HIGH",
                                "attackVector": "NETWORK",
                                "attackComplexity": "LOW",
                                "privilegesRequired": "NONE",
                                "userInteraction": "NONE",
                                "scope": "UNCHANGED",
                                "confidentialityImpact": "NONE",
                                "integrityImpact": "NONE",
                                "availabilityImpact": "HIGH",
                            },
                            "exploitabilityScore": 3.9,
                            "impactScore": 3.6,
                        }
                    ],
                    "cvssMetricV2": [
                        {
                            "source": "nvd@nist.gov",
                            "type": "Primary",
                            "cvssData": {
                                "version": "2.0",
                                "vectorString": "AV:N/AC:L/Au:N/C:N/I:N/A:P",
                                "baseScore": 5.0,
                                "accessVector": "NETWORK",
                                "accessComplexity": "LOW",
                                "authentication": "NONE",
                                "confidentialityImpact": "NONE",
                                "integrityImpact": "NONE",
                                "availabilityImpact": "PARTIAL",
                            },
                            "baseSeverity": "MEDIUM",
                            "exploitabilityScore": 10.0,
                            "impactScore": 2.9,
                            "acInsufInfo": False,
                            "obtainAllPrivilege": False,
                            "obtainUserPrivilege": False,
                            "obtainOtherPrivilege": False,
                            "userInteractionRequired": False,
                        }
                    ],
                },
                "weaknesses": [
                    {
                        "source": "josh@bress.net",
                        "type": "Secondary",
                        "description": [{"lang": "en", "value": "CWE-120"}],
                    },
                    {
                        "source": "nvd@nist.gov",
                        "type": "Primary",
                        "description": [{"lang": "en", "value": "CWE-787"}],
                    },
                ],
                "configurations": [
                    {
                        "nodes": [
                            {
                                "operator": "OR",
                                "negate": False,
                                "cpeMatch": [
                                    {
                                        "vulnerable": True,
                                        "criteria": "cpe:2.3:a:cherokee-project:cherokee_web_server:*:*:*:*:*:*:*:*",
                                        "versionEndIncluding": "1.2.103",
                                        "matchCriteriaId": "DCE1E311-F9E5-4752-9F51-D5DA78B7BBFA",
                                    }
                                ],
                            }
                        ]
                    }
                ],
                "references": [
                    {
                        "url": "https://i.imgur.com/PWCCyir.png",
                        "source": "josh@bress.net",
                        "tags": ["Exploit", "Third Party Advisory"],
                    },
                    {
                        "url": "https://i.imgur.com/PWCCyir.png",
                        "source": "af854a3a-2127-422b-91ae-364da2661108",
                        "tags": ["Exploit", "Third Party Advisory"],
                    },
                ],
            }
        }
    ],
}


def test_detect():
    parser = NVDCVEParser()
    assert parser.detect(test_data) is True


def test_detect_bad():
    parser = NVDCVEParser()
    assert parser.detect("some text") is False


def test_node_parse():
    parser = NVDCVEParser()
    parser.parse_data(test_data, populate=False)

    cve_df = parser.node_oriented_dfs["CVE"]
    assert len(cve_df.index) == 1

    org_df = parser.node_oriented_dfs["Organisation"]
    assert len(org_df.index) == 1

    cpe_df = parser.node_oriented_dfs["CPE"]
    assert len(cpe_df.index) == 1


def test_rel_parse():
    parser = NVDCVEParser()
    parser.parse_data(test_data, populate=False)

    org_to_cve_df = parser.rel_input_dfs["ORGANISATION_ASSIGNED_CVSS_TO_CVE"]["src_df"]
    assert len(org_to_cve_df.index) == 1

    cve_to_cpe_df = parser.rel_input_dfs["CVE_RELATES_TO_CPE"]["src_df"]
    assert len(cve_to_cpe_df.index) == 1


def test_populate(use_graph):
    parser = NVDCVEParser()
    parser.parse_data(test_data, populate=True)

    cypher = """MATCH (o:Organisation)-[:ORGANISATION_ASSIGNED_CVSS_TO_CVE]->(n:CVE)
                WHERE o.name = "NIST National Vulnerability Database"
                RETURN COUNT(DISTINCT n)"""
    assert use_graph.evaluate_query_single(cypher) == 1


def test_enrich_cve(monkeypatch, use_graph):
    def mockreturn(self, query):
        return test_data

    monkeypatch.setattr(NVDCVEOntolocyClient, "_query", mockreturn)

    enricher = NVDCVEEnricher()
    enricher.enrich("CVE-2019-1010218")

    cypher = """MATCH (o:Organisation)-[:ORGANISATION_ASSIGNED_CVSS_TO_CVE]->(n:CVE)
                WHERE o.name = "NIST National Vulnerability Database"
                RETURN COUNT(DISTINCT n)"""

    assert use_graph.evaluate_query_single(cypher) == 1


def test_cli_enrichment(use_graph, monkeypatch, cli_runner):
    def mockreturn(self, query):
        return test_data

    monkeypatch.setattr(NVDCVEOntolocyClient, "_query", mockreturn)

    result = cli_runner.invoke(cli, ["enrich", "cve", "nvd", "CVE-2019-1010218"])

    assert result.exit_code == 0
    assert "Enriching CVE-2019-1010218" in result.output

    cypher = """MATCH (o:Organisation)-[:ORGANISATION_ASSIGNED_CVSS_TO_CVE]->(n:CVE)
                WHERE o.name = "NIST National Vulnerability Database"
                RETURN COUNT(DISTINCT n)"""

    assert use_graph.evaluate_query_single(cypher) == 1
