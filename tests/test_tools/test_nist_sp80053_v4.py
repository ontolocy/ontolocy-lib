import pandas as pd
import pytest
import requests

from ontolocy.tools import NistSP80053v4Parser

test_data = pd.DataFrame(
    [
        {
            "FAMILY": "ACCESS CONTROL",
            "NAME": "AC-1",
            "TITLE": "ACCESS CONTROL POLICY AND PROCEDURES",
            "PRIORITY": "P1",
            "BASELINE-IMPACT": "LOW,MODERATE,HIGH",
            "DESCRIPTION": "The organization:",
            "SUPPLEMENTAL GUIDANCE": "This control addresses the establishment of policy and procedures for the effective implementation of selected security controls and control enhancements in the AC family. Policy and procedures reflect applicable federal laws, Executive Orders, directives, regulations, policies, standards, and guidance. Security program policies and procedures at the organization level may make the need for system-specific policies and procedures unnecessary. The policy can be included as part of the general information security policy for organizations or conversely, can be represented by multiple policies reflecting the complex nature of certain organizations. The procedures can be established for the security program in general and for particular information systems, if needed. The organizational risk management strategy is a key factor in establishing policy and procedures.",
            "RELATED": "PM-9",
        },
        {
            "FAMILY": None,
            "NAME": "AC-1a.",
            "TITLE": None,
            "PRIORITY": None,
            "BASELINE-IMPACT": None,
            "DESCRIPTION": "Develops, documents, and disseminates to [Assignment: organization-defined personnel or roles]:",
            "SUPPLEMENTAL GUIDANCE": None,
            "RELATED": None,
        },
        {
            "FAMILY": None,
            "NAME": "AC-1a.1.",
            "TITLE": None,
            "PRIORITY": None,
            "BASELINE-IMPACT": None,
            "DESCRIPTION": "An access control policy that addresses purpose, scope, roles, responsibilities, management commitment, coordination among organizational entities, and compliance; and",
            "SUPPLEMENTAL GUIDANCE": None,
            "RELATED": None,
        },
        {
            "FAMILY": None,
            "NAME": "AC-1a.2.",
            "TITLE": None,
            "PRIORITY": None,
            "BASELINE-IMPACT": None,
            "DESCRIPTION": "Procedures to facilitate the implementation of the access control policy and associated access controls; and",
            "SUPPLEMENTAL GUIDANCE": None,
            "RELATED": None,
        },
        {
            "FAMILY": None,
            "NAME": "AC-1b.",
            "TITLE": None,
            "PRIORITY": None,
            "BASELINE-IMPACT": None,
            "DESCRIPTION": "Reviews and updates the current:",
            "SUPPLEMENTAL GUIDANCE": None,
            "RELATED": None,
        },
        {
            "FAMILY": "ACCESS CONTROL",
            "NAME": "AC-2",
            "TITLE": "ACCOUNT MANAGEMENT",
            "PRIORITY": "P1",
            "BASELINE-IMPACT": "LOW,MODERATE,HIGH",
            "DESCRIPTION": "The organization:",
            "SUPPLEMENTAL GUIDANCE": "Information system account types include, for example, individual, shared, group, system, guest/anonymous, emergency, developer/manufacturer/vendor, temporary, and service. Some of the account management requirements listed above can be implemented by organizational information systems. The identification of authorized users of the information system and the specification of access privileges reflects the requirements in other security controls in the security plan. Users requiring administrative privileges on information system accounts receive additional scrutiny by appropriate organizational personnel (e.g., system owner, mission/business owner, or chief information security officer) responsible for approving such accounts and privileged access. Organizations may choose to define access privileges or other attributes by account, by type of account, or a combination of both. Other attributes required for authorizing access include, for example, restrictions on time-of-day, day-of-week, and point-of-origin. In defining other account attributes, organizations consider system-related requirements (e.g., scheduled mainteNonece, system upgrades) and mission/business requirements, (e.g., time zone differences, customer requirements, remote access to support travel requirements). Failure to consider these factors could affect information system availability. Temporary and emergency accounts are accounts intended for short-term use. Organizations establish temporary accounts as a part of normal account activation procedures when there is a need for short-term accounts without the demand for immediacy in account activation. Organizations establish emergency accounts in response to crisis situations and with the need for rapid account activation. Therefore, emergency account activation may bypass normal account authorization processes. Emergency and temporary accounts are not to be confused with infrequently used accounts (e.g., local logon accounts used for special tasks defined by organizations or when network resources are unavailable). Such accounts remain available and are not subject to automatic disabling or removal dates. Conditions for disabling or deactivating accounts include, for example: (i) when shared/group, emergency, or temporary accounts are no longer required; or (ii) when individuals are transferred or terminated. Some types of information system accounts may require specialized training.",
            "RELATED": "AC-3,AC-4,AC-5,AC-6,AC-10,AC-17,AC-19,AC-20,AU-9,IA-2,IA-4,IA-5,IA-8,CM-5,CM-6,CM-11,MA-3,MA-4,MA-5,PL-4,SC-13",
        },
        {
            "FAMILY": "ACCESS CONTROL",
            "NAME": "AC-2 (1)",
            "TITLE": "AUTOMATED SYSTEM ACCOUNT MANAGEMENT",
            "PRIORITY": None,
            "BASELINE-IMPACT": "MODERATE,HIGH",
            "DESCRIPTION": "The organization employs automated mechanisms to support the management of information system accounts.",
            "SUPPLEMENTAL GUIDANCE": "The use of automated mechanisms can include, for example: using email or text messaging to automatically notify account managers when users are terminated or transferred; using the information system to monitor account usage; and using telephonic notification to report atypical system account usage.",
            "RELATED": None,
        },
        {
            "FAMILY": "ACCESS CONTROL",
            "NAME": "AC-2 (2)",
            "TITLE": "REMOVAL OF TEMPORARY / EMERGENCY ACCOUNTS",
            "PRIORITY": None,
            "BASELINE-IMPACT": "MODERATE,HIGH",
            "DESCRIPTION": "The information system automatically [Selection: removes; disables] temporary and emergency accounts after [Assignment: organization-defined time period for each type of account].",
            "SUPPLEMENTAL GUIDANCE": "This control enhancement requires the removal of both temporary and emergency accounts automatically after a predefined period of time has elapsed, rather than at the convenience of the systems administrator.",
            "RELATED": None,
        },
        {
            "FAMILY": "ACCESS CONTROL",
            "NAME": "AC-2 (3)",
            "TITLE": "DISABLE INACTIVE ACCOUNTS",
            "PRIORITY": None,
            "BASELINE-IMPACT": "MODERATE,HIGH",
            "DESCRIPTION": "The information system automatically disables inactive accounts after [Assignment: organization-defined time period].",
            "SUPPLEMENTAL GUIDANCE": None,
            "RELATED": None,
        },
        {
            "FAMILY": None,
            "NAME": "PM-15b.",
            "TITLE": None,
            "PRIORITY": None,
            "BASELINE-IMPACT": None,
            "DESCRIPTION": "To maintain currency with recommended security practices, techniques, and technologies; and",
            "SUPPLEMENTAL GUIDANCE": None,
            "RELATED": None,
        },
        {
            "FAMILY": None,
            "NAME": "PM-15c.",
            "TITLE": None,
            "PRIORITY": None,
            "BASELINE-IMPACT": None,
            "DESCRIPTION": "To share current security-related information including threats, vulnerabilities, and incidents.",
            "SUPPLEMENTAL GUIDANCE": None,
            "RELATED": None,
        },
        {
            "FAMILY": "PROGRAM MANAGEMENT",
            "NAME": "PM-16",
            "TITLE": "THREAT AWARENESS PROGRAM",
            "PRIORITY": None,
            "BASELINE-IMPACT": None,
            "DESCRIPTION": "The organization implements a threat awareness program that includes a cross-organization information-sharing capability.",
            "SUPPLEMENTAL GUIDANCE": "Because of the constantly changing and increasing sophistication of adversaries, especially the advanced persistent threat (APT), it is becoming more likely that adversaries may successfully breach or compromise organizational information systems. One of the best techniques to address this concern is for organizations to share threat information. This can include, for example, sharing threat events (i.e., tactics, techniques, and procedures) that organizations have experienced, mitigations that organizations have found are effective against certain types of threats, threat intelligence (i.e., indications and warnings about threats that are likely to occur). Threat information sharing may be bilateral (e.g., government-commercial cooperatives, government-government cooperatives), or multilateral (e.g., organizations taking part in threat-sharing consortia). Threat information may be highly sensitive requiring special agreements and protection, or less sensitive and freely shared.",
            "RELATED": "PM-12,PM-16",
        },
    ]
)


def test_detect():
    parser = NistSP80053v4Parser()

    assert parser.detect(test_data) is True


def test_detect_bad():
    parser = NistSP80053v4Parser()

    assert parser.detect("just some text") is False


def test_node_parse():
    parser = NistSP80053v4Parser()
    parser.parse_data(test_data, populate=False)

    node_df = parser.node_oriented_dfs["Control"]

    # there are 12 controls in the test data
    # plus 18 families defined by the parser
    assert len(node_df.index) == 30


def test_rel_parse():
    parser = NistSP80053v4Parser()
    parser.parse_data(test_data, populate=False)

    parents_df = parser.rel_input_dfs["CONTROL_HAS_PARENT_CONTROL"]["src_df"]

    assert len(parents_df.index) == 12


def test_populate(use_graph):
    parser = NistSP80053v4Parser()
    parser.parse_data(test_data, populate=True)

    ctrl_cypher = """MATCH (n:Control) RETURN COUNT(DISTINCT n)"""

    assert use_graph.evaluate_query_single(ctrl_cypher) == 30

    rel_cypher = """MATCH (:Control)-[r:CONTROL_HAS_PARENT_CONTROL]->(:Control) RETURN COUNT(DISTINCT r)"""

    assert use_graph.evaluate_query_single(rel_cypher) == 12


@pytest.mark.webtest
def test_parse_web():
    parser = NistSP80053v4Parser()
    parser.parse_url(
        "https://csrc.nist.gov/csrc/media/Projects/risk-management/800-53%20Downloads/800-53r4/800-53-rev4-controls.csv",
        populate=False,
    )

    node_df = parser.node_oriented_dfs["Control"]

    # there are 1682 controls in the framework
    # plus 18 families defined by the parser
    assert len(node_df.index) == 1682 + 18

    parents_df = parser.rel_input_dfs["CONTROL_HAS_PARENT_CONTROL"]["src_df"]

    assert len(parents_df.index) == 1682


@pytest.mark.slow
@pytest.mark.webtest
def test_populate_web(use_graph):
    parser = NistSP80053v4Parser()
    parser.parse_url(
        "https://csrc.nist.gov/csrc/media/Projects/risk-management/800-53%20Downloads/800-53r4/800-53-rev4-controls.csv",
        populate=True,
    )

    ctrl_cypher = """MATCH (n:Control) RETURN COUNT(DISTINCT n)"""

    assert use_graph.evaluate_query_single(ctrl_cypher) == 1682 + 18

    rel_cypher = """MATCH (:Control)-[r:CONTROL_HAS_PARENT_CONTROL]->(:Control) RETURN COUNT(DISTINCT r)"""

    assert use_graph.evaluate_query_single(rel_cypher) == 1682


@pytest.mark.slow
@pytest.mark.webtest
def test_populate_file(use_graph, tmp_path):
    tmp_file = tmp_path / "sp80053.4.xlsx"

    url = "https://csrc.nist.gov/csrc/media/Projects/risk-management/800-53%20Downloads/800-53r4/800-53-rev4-controls.csv"
    response = requests.get(url)

    with open(tmp_file, "wb") as file:
        file.write(response.content)

    parser = NistSP80053v4Parser()
    parser.parse_file(str(tmp_file), populate=True)

    ctrl_cypher = """MATCH (n:Control) RETURN COUNT(DISTINCT n)"""

    assert use_graph.evaluate_query_single(ctrl_cypher) == 1682 + 18

    rel_cypher = """MATCH (:Control)-[r:CONTROL_HAS_PARENT_CONTROL]->(:Control) RETURN COUNT(DISTINCT r)"""

    assert use_graph.evaluate_query_single(rel_cypher) == 1682
