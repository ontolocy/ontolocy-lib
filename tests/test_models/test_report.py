from pydantic import HttpUrl

from ontolocy import Report, ReportMentionsCVE
from ontolocy.models.cve import CVE

report = Report(
    title="My First Report",
    author="Test Author",
    url_reference="https://example.com",
    published_date="2022-09-01",
    summary="This is just a test",
)


report2 = Report(
    title="My Second Report",
    author="Test Author",
    url_reference="https://example.com/#report",
    published_date="2022-10-01",
    summary="This is just a test",
    additional_urls=["https://example.com/#1", "https://example.com/#2"],
    unique_id="my-second-report",
)


def test_report():
    assert report.get_pp() == "bbaecd6b-ab55-5bd3-8cc7-b415cb8b7a29"


def test_report2():
    assert report2.get_pp() == "my-second-report"
    assert report2.additional_urls[1] == HttpUrl("https://example.com/#2")


def test_report_mentions_cve(use_graph):
    report.merge()

    cve = CVE(cve_id="CVE-2021-44832")
    cve.create()

    rel = ReportMentionsCVE(source=report, target=cve)
    rel.merge()

    cypher = """
    MATCH (report:Report)-[r:REPORT_MENTIONS_CVE]->(cve:CVE)
    WHERE report.unique_id = $unique_id
    RETURN COUNT(DISTINCT r)
    """

    params = {"unique_id": str(report.get_pp())}

    result = use_graph.evaluate_query_single(cypher, params)

    assert result == 1
