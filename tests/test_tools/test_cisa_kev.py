import pytest

from ontolocy.tools import CisaKevParser

test_data = """cveID,vendorProject,product,vulnerabilityName,dateAdded,shortDescription,requiredAction,dueDate,knownRansomwareCampaignUse,notes,cwes
CVE-2025-23006,SonicWall,"SMA1000 Appliances","SonicWall SMA1000 Appliances Deserialization Vulnerability",2025-01-24,"SonicWall SMA1000 Appliance Management Console (AMC) and Central Management Console (CMC) contain a deserialization of untrusted data vulnerability, which can enable a remote, unauthenticated attacker to execute arbitrary OS commands.","Apply mitigations per vendor instructions or discontinue use of the product if mitigations are unavailable.",2025-02-14,Unknown,"https://psirt.global.sonicwall.com/vuln-detail/SNWLID-2025-0002 ; https://nvd.nist.gov/vuln/detail/CVE-2025-23006",CWE-502
CVE-2020-11023,JQuery,JQuery,"JQuery Cross-Site Scripting (XSS) Vulnerability",2025-01-23,"JQuery contains a persistent cross-site scripting (XSS) vulnerability. When passing maliciously formed, untrusted input enclosed in HTML tags, JQuery's DOM manipulators can execute untrusted code in the context of the user's browser.","Apply mitigations per vendor instructions or discontinue use of the product if mitigations are unavailable.",2025-02-13,Unknown,"https://blog.jquery.com/2020/04/10/jquery-3-5-0-released/ ; https://nvd.nist.gov/vuln/detail/CVE-2020-11023",CWE-79
CVE-2024-50603,Aviatrix,Controllers,"Aviatrix Controllers OS Command Injection Vulnerability",2025-01-16,"Aviatrix Controllers contain an OS command injection vulnerability that could allow an unauthenticated attacker to execute arbitrary code. Shell metacharacters can be sent to /v1/api in cloud_type for list_flightpath_destination_instances, or src_cloud_type for flightpath_connection_test.","Apply mitigations per vendor instructions or discontinue use of the product if mitigations are unavailable.",2025-02-06,Unknown,"https://docs.aviatrix.com/documentation/latest/release-notices/psirt-advisories/psirt-advisories.html?expand=true ; https://nvd.nist.gov/vuln/detail/CVE-2024-50603",CWE-78
CVE-2025-21335,Microsoft,Windows,"Microsoft Windows Hyper-V NT Kernel Integration VSP Use-After-Free Vulnerability",2025-01-14,"Microsoft Windows Hyper-V NT Kernel Integration VSP contains a use-after-free vulnerability that allows a local attacker to gain SYSTEM privileges.","Apply mitigations per vendor instructions or discontinue use of the product if mitigations are unavailable.",2025-02-04,Unknown,"https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2025-21335 ; https://nvd.nist.gov/vuln/detail/CVE-2025-21335",CWE-416
CVE-2025-21334,Microsoft,Windows,"Microsoft Windows Hyper-V NT Kernel Integration VSP Use-After-Free Vulnerability",2025-01-14,"Microsoft Windows Hyper-V NT Kernel Integration VSP contains a use-after-free vulnerability that allows a local attacker to gain SYSTEM privileges.","Apply mitigations per vendor instructions or discontinue use of the product if mitigations are unavailable.",2025-02-04,Unknown,"https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2025-21334 ; https://nvd.nist.gov/vuln/detail/CVE-2025-21334",CWE-416"""


def test_detect():
    parser = CisaKevParser()

    input_data = parser._load_data(test_data)

    assert parser.detect(input_data) is True


def test_detect_bad():
    parser = CisaKevParser()

    assert parser.detect("just some text") is False


def test_node_parse():
    parser = CisaKevParser()

    input_data = parser._load_data(test_data)
    parser.parse_data(input_data, populate=False)

    cve_df = parser.node_oriented_dfs["CVE"]

    assert len(cve_df.index) == 5

    org_df = parser.node_oriented_dfs["Organisation"]

    assert len(org_df.index) == 1


def test_rel_parse():
    parser = CisaKevParser()

    input_data = parser._load_data(test_data)
    parser.parse_data(input_data, populate=False)

    org_to_cve_df = parser.rel_input_dfs["ORGANISATION_REPORTED_EXPLOITATION_OF_CVE"][
        "src_df"
    ]
    assert len(org_to_cve_df.index) == 5


def test_populate(use_graph):
    parser = CisaKevParser()

    input_data = parser._load_data(test_data)
    parser.parse_data(input_data, populate=True)

    cypher = """MATCH (:Organisation)-[:ORGANISATION_REPORTED_EXPLOITATION_OF_CVE]->(n:CVE) RETURN COUNT(DISTINCT n)"""

    assert use_graph.evaluate_query_single(cypher) == 5


@pytest.mark.slow
@pytest.mark.webtest
def test_populate_web(use_graph):
    parser = CisaKevParser()

    parser.parse_url(
        "https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv",
        populate=True,
    )

    cypher = """MATCH (cve:CVE) WHERE cve.cve_id = 'CVE-2019-0708' RETURN COUNT(DISTINCT cve)"""

    # check for a specific CVE (BlueKeep) which should be in the dataset
    assert use_graph.evaluate_query_single(cypher) == 1

    cypher = """MATCH (:Organisation)-[:ORGANISATION_REPORTED_EXPLOITATION_OF_CVE]->(n:CVE) RETURN COUNT(DISTINCT n)"""

    # the list is always growing, so we can't check for a specific number
    assert use_graph.evaluate_query_single(cypher) > 1200
