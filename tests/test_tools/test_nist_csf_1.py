import pandas as pd
import pytest
import requests

from ontolocy.tools import NistCSF1Parser

test_data = pd.DataFrame(
    [
        {
            "Function": "IDENTIFY (ID)",
            "Category": "Asset Management (ID.AM): The data, personnel, devices, systems, and facilities that enable the organization to achieve business purposes are identified and managed consistent with their relative importance to organizational objectives and the organization’s risk strategy.",
            "Subcategory": "ID.AM-1: Physical devices and systems within the organization are inventoried",
            "Informative References": "·\xa0\xa0\xa0\xa0\xa0\xa0 CIS CSC 1",
        },
        {
            "Function": None,
            "Category": None,
            "Subcategory": None,
            "Informative References": "·\xa0\xa0\xa0\xa0\xa0\xa0 COBIT 5 BAI09.01, BAI09.02",
        },
        {
            "Function": None,
            "Category": None,
            "Subcategory": None,
            "Informative References": "·\xa0\xa0\xa0\xa0\xa0\xa0 ISA 62443-2-1:2009 4.2.3.4",
        },
        {
            "Function": None,
            "Category": None,
            "Subcategory": None,
            "Informative References": "·\xa0\xa0\xa0\xa0\xa0\xa0 ISA 62443-3-3:2013 SR 7.8",
        },
        {
            "Function": None,
            "Category": None,
            "Subcategory": None,
            "Informative References": "·\xa0\xa0\xa0\xa0\xa0\xa0 ISO/IEC 27001:2013 A.8.1.1, A.8.1.2",
        },
        {
            "Function": None,
            "Category": None,
            "Subcategory": None,
            "Informative References": "·\xa0\xa0\xa0\xa0\xa0\xa0 NIST SP 800-53 Rev. 4 CM-8, PM-5",
        },
        {
            "Function": None,
            "Category": None,
            "Subcategory": "ID.AM-2: Software platforms and applications within the organization are inventoried",
            "Informative References": "·\xa0\xa0\xa0\xa0\xa0\xa0 CIS CSC 2",
        },
        {
            "Function": None,
            "Category": None,
            "Subcategory": None,
            "Informative References": "·\xa0\xa0\xa0\xa0\xa0\xa0 COBIT 5 BAI09.01, BAI09.02, BAI09.05",
        },
        {
            "Function": None,
            "Category": None,
            "Subcategory": None,
            "Informative References": "·\xa0\xa0\xa0\xa0\xa0\xa0 ISA 62443-2-1:2009 4.2.3.4",
        },
        {
            "Function": None,
            "Category": None,
            "Subcategory": None,
            "Informative References": "·\xa0\xa0\xa0\xa0\xa0\xa0 ISA 62443-3-3:2013 SR 7.8",
        },
        {
            "Function": "PROTECT (PR)",
            "Category": "Identity Management, Authentication and Access Control (PR.AC): Access to physical and logical assets and associated facilities is limited to authorized users, processes, and devices, and is managed consistent with the assessed risk of unauthorized access to authorized activities and transactions.",
            "Subcategory": "PR.AC-1: Identities and credentials are issued, managed, verified, revoked, and audited for authorized devices, users and processes",
            "Informative References": "·\xa0\xa0\xa0\xa0\xa0\xa0 CIS CSC 1, 5, 15, 16",
        },
        {
            "Function": "DETECT (DE)",
            "Category": "Anomalies and Events (DE.AE): Anomalous activity is detected and the potential impact of events is understood.",
            "Subcategory": "DE.AE-1: A baseline of network operations and expected data flows for users and systems is established and managed",
            "Informative References": "·\xa0\xa0\xa0\xa0\xa0\xa0 CIS CSC 1, 4, 6, 12, 13, 15, 16",
        },
        {
            "Function": "RESPOND (RS)",
            "Category": "Response Planning (RS.RP): Response processes and procedures are executed and maintained, to ensure response to detected cybersecurity incidents.",
            "Subcategory": "RS.RP-1: Response plan is executed during or after an incident",
            "Informative References": "·\xa0\xa0\xa0\xa0\xa0\xa0 CIS CSC 19",
        },
        {
            "Function": "RECOVER (RC)",
            "Category": "Recovery Planning (RC.RP): Recovery processes and procedures are executed and maintained to ensure restoration of systems or assets affected by cybersecurity incidents.",
            "Subcategory": "RC.RP-1: Recovery plan is executed during or after a cybersecurity incident ",
            "Informative References": "·\xa0\xa0\xa0\xa0\xa0\xa0 CIS CSC 10",
        },
        {
            "Function": None,
            "Category": "Information Protection Processes and Procedures (PR.IP): Security policies (that address purpose, scope, roles, responsibilities, management commitment, and coordination among organizational entities), processes, and procedures are maintained and used to manage protection of information systems and assets.",
            "Subcategory": "PR.IP-1: A baseline configuration of information technology/industrial control systems is created and maintained incorporating security principles (e.g. concept of least functionality)",
            "Informative References": "·\xa0\xa0\xa0\xa0\xa0\xa0 CIS CSC 3, 9, 11",
        },
        {
            "Function": None,
            "Category": None,
            "Subcategory": "PR.IP-10: Response and recovery plans are tested",
            "Informative References": "·\xa0\xa0\xa0\xa0\xa0\xa0 CIS CSC 19, 20",
        },
        {
            "Function": None,
            "Category": None,
            "Subcategory": "PR.IP-12: A vulnerability management plan is developed and implemented",
            "Informative References": "·\xa0\xa0\xa0\xa0\xa0\xa0 CIS CSC 4, 18, 20",
        },
    ]
)


def test_detect():
    parser = NistCSF1Parser()

    assert parser.detect(test_data) is True


def test_detect_bad():
    parser = NistCSF1Parser()

    assert parser.detect("just some text") is False


def test_node_parse():
    parser = NistCSF1Parser()
    parser.parse_data(test_data, populate=False)

    node_df = parser.node_oriented_dfs["Control"]

    assert len(node_df.index) == 20


def test_rel_parse():
    parser = NistCSF1Parser()
    parser.parse_data(test_data, populate=False)

    parents_df = parser.rel_input_dfs["CONTROL_HAS_PARENT_CONTROL"]["src_df"]

    assert len(parents_df.index) == 15


def test_populate(use_graph):
    parser = NistCSF1Parser()
    parser.parse_data(test_data, populate=True)

    ctrl_cypher = """MATCH (n:Control) RETURN COUNT(DISTINCT n)"""

    assert use_graph.evaluate_query_single(ctrl_cypher) == 20

    rel_cypher = """MATCH (:Control)-[r:CONTROL_HAS_PARENT_CONTROL]->(:Control) RETURN COUNT(DISTINCT r)"""

    assert use_graph.evaluate_query_single(rel_cypher) == 15


@pytest.mark.slow
@pytest.mark.webtest
def test_populate_web(use_graph):
    parser = NistCSF1Parser()
    parser.parse_url(
        "https://www.nist.gov/document/2018-04-16frameworkv11core1xlsx", populate=True
    )

    ctrl_cypher = """MATCH (n:Control) RETURN COUNT(DISTINCT n)"""

    assert use_graph.evaluate_query_single(ctrl_cypher) == 136

    rel_cypher = """MATCH (:Control)-[r:CONTROL_HAS_PARENT_CONTROL]->(:Control) RETURN COUNT(DISTINCT r)"""

    assert use_graph.evaluate_query_single(rel_cypher) == 131


@pytest.mark.slow
@pytest.mark.webtest
def test_populate_file(use_graph, tmp_path):
    tmp_file = tmp_path / "csf1.xlsx"

    url = "https://www.nist.gov/document/2018-04-16frameworkv11core1xlsx"
    response = requests.get(url)

    with open(tmp_file, "wb") as file:
        file.write(response.content)

    parser = NistCSF1Parser()
    parser.parse_file(str(tmp_file), populate=True)

    ctrl_cypher = """MATCH (n:Control) RETURN COUNT(DISTINCT n)"""

    assert use_graph.evaluate_query_single(ctrl_cypher) == 136

    rel_cypher = """MATCH (:Control)-[r:CONTROL_HAS_PARENT_CONTROL]->(:Control) RETURN COUNT(DISTINCT r)"""

    assert use_graph.evaluate_query_single(rel_cypher) == 131
