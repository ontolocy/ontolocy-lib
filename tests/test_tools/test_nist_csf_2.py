import pandas as pd
import pytest
import requests

from ontolocy.tools import NistCSF2Parser

test_data = pd.DataFrame(
    [
        {
            "Function": "GOVERN (GV): The organization's cybersecurity risk management strategy, expectations, and policy are established, communicated, and monitored",
            "Category": None,
            "Subcategory": None,
            "Implementation Examples": None,
            "Informative References": "CRI Profile v2.0: GV\nCSF v1.1: ID.GV\nSP 800-221A: GV.PO",
        },
        {
            "Function": None,
            "Category": "Organizational Context (GV.OC): The circumstances - mission, stakeholder expectations, dependencies, and legal, regulatory, and contractual requirements - surrounding the organization's cybersecurity risk management decisions are understood",
            "Subcategory": None,
            "Implementation Examples": None,
            "Informative References": "CRI Profile v2.0: GV.OC\nCSF v1.1: ID.BE\nSP 800-221A: GV.CT\nSP 800-221A: GV.CT-5",
        },
        {
            "Function": None,
            "Category": None,
            "Subcategory": "GV.OC-01: The organizational mission is understood and informs cybersecurity risk management",
            "Implementation Examples": "Ex1: Share the organization's mission (e.g., through vision and mission statements, marketing, and service strategies) to provide a basis for identifying risks that may impede that mission",
            "Informative References": "CCMv4.0: BCR-01\nCCMv4.0: BCR-07\nCRI Profile v2.0: GV.OC-01\nCRI Profile v2.0: GV.OC-01.01\nCSF v1.1: ID.BE-2\nCSF v1.1: ID.BE-3\nSP 800-221A: GV.CT-5\nSP 800-221A: GV.CT-3\nSP 800-53 Rev 5.1.1: PM-11",
        },
        {
            "Function": None,
            "Category": None,
            "Subcategory": "GV.OC-02: Internal and external stakeholders are understood, and their needs and expectations regarding cybersecurity risk management are understood and considered",
            "Implementation Examples": "Ex1: Identify relevant internal stakeholders and their cybersecurity-related expectations (e.g., performance and risk expectations of officers, directors, and advisors; cultural expectations of employees)\nEx2: Identify relevant external stakeholders and their cybersecurity-related expectations (e.g., privacy expectations of customers, business expectations of partnerships, compliance expectations of regulators, ethics expectations of society)",
            "Informative References": "CCMv4.0: STA-08\nCCMv4.0: STA-13\nCRI Profile v2.0: GV.OC-02\nCRI Profile v2.0: GV.OC-02.01\nCRI Profile v2.0: GV.OC-02.02\nCRI Profile v2.0: GV.OC-02.03\nCSF v1.1: ID.SC-2\nCSF v1.1: ID.GV-2\nSP 800-218: PO.2.1\nSP 800-221A: GV.OV-2\nSP 800-221A: GV.CT-2\nSP 800-221A: GV.CT-3\nSP 800-53 Rev 5.1.1: PM-09\nSP 800-53 Rev 5.1.1: PM-18\nSP 800-53 Rev 5.1.1: PM-30\nSP 800-53 Rev 5.1.1: SR-03\nSP 800-53 Rev 5.1.1: SR-05\nSP 800-53 Rev 5.1.1: SR-06\nSP 800-53 Rev 5.1.1: SR-08",
        },
        {
            "Function": None,
            "Category": None,
            "Subcategory": "GV.OC-03: Legal, regulatory, and contractual requirements regarding cybersecurity - including privacy and civil liberties obligations - are understood and managed",
            "Implementation Examples": "Ex1: Determine a process to track and manage legal and regulatory requirements regarding protection of individuals' information (e.g., Health Insurance Portability and Accountability Act, California Consumer Privacy Act, General Data Protection Regulation)\nEx2: Determine a process to track and manage contractual requirements for cybersecurity management of supplier, customer, and partner information\nEx3: Align the organization's cybersecurity strategy with legal, regulatory, and contractual requirements",
            "Informative References": "CCMv4.0: CEK-12\nCCMv4.0: CEK-13\nCCMv4.0: CEK-14\nCCMv4.0: CEK-15\nCCMv4.0: CEK-16\nCCMv4.0: CEK-17\nCCMv4.0: CEK-18\nCCMv4.0: CEK-19\nCCMv4.0: CEK-20\nCCMv4.0: CEK-21\nCCMv4.0: DSP-01\nCCMv4.0: DSP-10\nCCMv4.0: DSP-11\nCCMv4.0: DSP-12\nCCMv4.0: DSP-16\nCCMv4.0: DSP-18\nCCMv4.0: GRC-07\nCCMv4.0: HRS-13\nCCMv4.0: STA-05\nCCMv4.0: STA-13\nCRI Profile v2.0: GV.OC-03\nCRI Profile v2.0: GV.OC-03.01\nCRI Profile v2.0: GV.OC-03.02\nCSF v1.1: ID.GV-3\nSP 800-218: PO.1.1\nSP 800-218: PO.1.2\nSP 800-53 Rev 5.1.1: AC-01\nSP 800-53 Rev 5.1.1: AT-01\nSP 800-53 Rev 5.1.1: AU-01\nSP 800-53 Rev 5.1.1: CA-01\nSP 800-53 Rev 5.1.1: CM-01\nSP 800-53 Rev 5.1.1: CP-01\nSP 800-53 Rev 5.1.1: IA-01\nSP 800-53 Rev 5.1.1: IR-01\nSP 800-53 Rev 5.1.1: MA-01\nSP 800-53 Rev 5.1.1: MP-01\nSP 800-53 Rev 5.1.1: PE-01\nSP 800-53 Rev 5.1.1: PL-01\nSP 800-53 Rev 5.1.1: PM-01\nSP 800-53 Rev 5.1.1: PS-01\nSP 800-53 Rev 5.1.1: PT-01\nSP 800-53 Rev 5.1.1: RA-01\nSP 800-53 Rev 5.1.1: SA-01\nSP 800-53 Rev 5.1.1: SC-01\nSP 800-53 Rev 5.1.1: SI-01\nSP 800-53 Rev 5.1.1: SR-01\nSP 800-53 Rev 5.1.1: PM-28\nSP 800-53 Rev 5.1.1: PT",
        },
        {
            "Function": "GOVERN (GV): The organization's cybersecurity risk management strategy, expectations, and policy are established, communicated, and monitored",
            "Category": None,
            "Subcategory": None,
            "Implementation Examples": None,
            "Informative References": "CRI Profile v2.0: GV\nCSF v1.1: ID.GV\nSP 800-221A: GV.PO",
        },
        {
            "Function": "GOVERN (GV)",
            "Category": None,
            "Subcategory": None,
            "Implementation Examples": None,
            "Informative References": None,
        },
        {
            "Function": "IDENTIFY (ID): The organization's current cybersecurity risks are understood",
            "Category": None,
            "Subcategory": None,
            "Implementation Examples": None,
            "Informative References": "CRI Profile v2.0: ID\nCSF v1.1: ID",
        },
        {
            "Function": "IDENTIFY (ID)",
            "Category": None,
            "Subcategory": None,
            "Implementation Examples": None,
            "Informative References": None,
        },
        {
            "Function": "PROTECT (PR): Safeguards to manage the organization's cybersecurity risks are used",
            "Category": None,
            "Subcategory": None,
            "Implementation Examples": None,
            "Informative References": "CRI Profile v2.0: PR\nCSF v1.1: PR",
        },
    ]
)


def test_detect():
    parser = NistCSF2Parser()

    assert parser.detect(test_data) is True


def test_detect_bad():
    parser = NistCSF2Parser()

    assert parser.detect("just some text") is False


def test_node_parse():
    parser = NistCSF2Parser()
    parser.parse_data(test_data, populate=False)

    node_df = parser.node_oriented_dfs["Control"]

    assert len(node_df.index) == 7


def test_rel_parse():
    parser = NistCSF2Parser()
    parser.parse_data(test_data, populate=False)

    parents_df = parser.rel_input_dfs["CONTROL_HAS_PARENT_CONTROL"]["src_df"]

    assert len(parents_df.index) == 4


def test_populate(use_graph):
    parser = NistCSF2Parser()
    parser.parse_data(test_data, populate=True)

    ctrl_cypher = """MATCH (n:Control) RETURN COUNT(DISTINCT n)"""

    assert use_graph.evaluate_query_single(ctrl_cypher) == 7

    rel_cypher = """MATCH (:Control)-[r:CONTROL_HAS_PARENT_CONTROL]->(:Control) RETURN COUNT(DISTINCT r)"""

    assert use_graph.evaluate_query_single(rel_cypher) == 4


@pytest.mark.webtest
def test_parse_web():
    parser = NistCSF2Parser()
    parser.parse_url(
        "https://csrc.nist.gov/extensions/nudp/services/json/csf/download?olirids=all",
        populate=False,
    )

    node_df = parser.node_oriented_dfs["Control"]

    assert len(node_df.index) == 134

    parents_df = parser.rel_input_dfs["CONTROL_HAS_PARENT_CONTROL"]["src_df"]

    assert len(parents_df.index) == 128


@pytest.mark.slow
@pytest.mark.webtest
def test_populate_web(use_graph):
    parser = NistCSF2Parser()
    parser.parse_url(
        "https://csrc.nist.gov/extensions/nudp/services/json/csf/download?olirids=all",
        populate=True,
    )

    ctrl_cypher = """MATCH (n:Control) RETURN COUNT(DISTINCT n)"""

    assert use_graph.evaluate_query_single(ctrl_cypher) == 134

    rel_cypher = """MATCH (:Control)-[r:CONTROL_HAS_PARENT_CONTROL]->(:Control) RETURN COUNT(DISTINCT r)"""

    assert use_graph.evaluate_query_single(rel_cypher) == 128


@pytest.mark.slow
@pytest.mark.webtest
def test_populate_file(use_graph, tmp_path):
    tmp_file = tmp_path / "csf.1.xlsx"

    url = "https://csrc.nist.gov/extensions/nudp/services/json/csf/download?olirids=all"
    response = requests.get(url)

    with open(tmp_file, "wb") as file:
        file.write(response.content)

    parser = NistCSF2Parser()
    parser.parse_file(str(tmp_file), populate=True)

    ctrl_cypher = """MATCH (n:Control) RETURN COUNT(DISTINCT n)"""

    assert use_graph.evaluate_query_single(ctrl_cypher) == 134

    rel_cypher = """MATCH (:Control)-[r:CONTROL_HAS_PARENT_CONTROL]->(:Control) RETURN COUNT(DISTINCT r)"""

    assert use_graph.evaluate_query_single(rel_cypher) == 128
