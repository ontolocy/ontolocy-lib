from ontolocy import Report, ReportMentionsCVE
from ontolocy.models.cve import CVE

report = Report(
    title="My First Report",
    author="Test Author",
    url_reference="https://example.com",
    published_date="2022-09-01",
    summary="This is just a test",
)


def test_report():
    assert report.get_primary_property_value() == "https://example.com/"


def test_report_mentions_cve(use_graph):
    report.merge()

    cve = CVE(cve_id="CVE-2021-44832")
    cve.create()

    rel = ReportMentionsCVE(source=report, target=cve)
    rel.merge()

    cypher = f"""
    MATCH (report:Report)-[r:REPORT_MENTIONS_CVE]->(cve:CVE)
    WHERE report.url_reference = $url_reference
    RETURN COUNT(DISTINCT r)
    """

    params = {"url_reference": str(report.get_primary_property_value())}

    result = use_graph.evaluate_query_single(cypher, params)

    assert result == 1
