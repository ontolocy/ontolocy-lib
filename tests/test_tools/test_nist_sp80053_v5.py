import pandas as pd
import pytest
import requests

from ontolocy.tools import NistSP80053v5Parser

test_data = pd.DataFrame(
    [
        {
            "Control Identifier": "AC-1",
            "Control (or Control Enhancement) Name": "Policy and Procedures",
            "Control Text": "a. Develop, document, and disseminate to [Assignment: organization-defined personnel or roles]:\n1. [Selection (one or more): Organization-level; Mission/business process-level; System-level] access control policy that:\n(a) Addresses purpose, scope, roles, responsibilities, management commitment, coordination among organizational entities, and compliance; and\n(b) Is consistent with applicable laws, executive orders, directives, regulations, policies, standards, and guidelines; and\n2. Procedures to facilitate the implementation of the access control policy and the associated access controls;\nb. Designate an [Assignment: organization-defined official] to manage the development, documentation, and dissemination of the access control policy and procedures; and\nc. Review and update the current access control:\n1. Policy [Assignment: organization-defined frequency] and following [Assignment: organization-defined events]; and\n2. Procedures [Assignment: organization-defined frequency] and following [Assignment: organization-defined events].",
            "Discussion": "Access control policy and procedures address the controls in the AC family that are implemented within systems and organizations. The risk management strategy is an important factor in establishing such policies and procedures. Policies and procedures contribute to security and privacy assurance. Therefore, it is important that security and privacy programs collaborate on the development of access control policy and procedures. Security and privacy program policies and procedures at the organization level are preferable, in general, and may obviate the need for mission- or system-specific policies and procedures. The policy can be included as part of the general security and privacy policy or be represented by multiple policies reflecting the complex nature of organizations. Procedures can be established for security and privacy programs, for mission or business processes, and for systems, if needed. Procedures describe how the policies or controls are implemented and can be directed at the individual or role that is the object of the procedure. Procedures can be documented in system security and privacy plans or in one or more separate documents. Events that may precipitate an update to access control policy and procedures include assessment or audit findings, security incidents or breaches, or changes in laws, executive orders, directives, regulations, policies, standards, and guidelines. Simply restating controls does not constitute an organizational policy or procedure.",
            "Related Controls": "IA-1, PM-9, PM-24, PS-8, SI-12 .",
        },
        {
            "Control Identifier": "AC-2",
            "Control (or Control Enhancement) Name": "Account Management",
            "Control Text": "a. Define and document the types of accounts allowed and specifically prohibited for use within the system;\nb. Assign account managers;\nc. Require [Assignment: organization-defined prerequisites and criteria] for group and role membership;\nd. Specify:\n1. Authorized users of the system;\n2. Group and role membership; and\n3. Access authorizations (i.e., privileges) and [Assignment: organization-defined attributes (as required)] for each account;\ne. Require approvals by [Assignment: organization-defined personnel or roles] for requests to create accounts;\nf. Create, enable, modify, disable, and remove accounts in accordance with [Assignment: organization-defined policy, procedures, prerequisites, and criteria];\ng. Monitor the use of accounts;\nh. Notify account managers and [Assignment: organization-defined personnel or roles] within:\n1. [Assignment: organization-defined time period] when accounts are no longer required;\n2. [Assignment: organization-defined time period] when users are terminated or transferred; and\n3. [Assignment: organization-defined time period] when system usage or need-to-know changes for an individual;\ni. Authorize access to the system based on:\n1. A valid access authorization;\n2. Intended system usage; and\n3. [Assignment: organization-defined attributes (as required)];\nj. Review accounts for compliance with account management requirements [Assignment: organization-defined frequency];\nk. Establish and implement a process for changing shared or group account authenticators (if deployed) when individuals are removed from the group; and\nl. Align account management processes with personnel termination and transfer processes.",
            "Discussion": "Examples of system account types include individual, shared, group, system, guest, anonymous, emergency, developer, temporary, and service. Identification of authorized system users and the specification of access privileges reflect the requirements in other controls in the security plan. Users requiring administrative privileges on system accounts receive additional scrutiny by organizational personnel responsible for approving such accounts and privileged access, including system owner, mission or business owner, senior agency information security officer, or senior agency official for privacy. Types of accounts that organizations may wish to prohibit due to increased risk include shared, group, emergency, anonymous, temporary, and guest accounts.\nWhere access involves personally identifiable information, security programs collaborate with the senior agency official for privacy to establish the specific conditions for group and role membership; specify authorized users, group and role membership, and access authorizations for each account; and create, adjust, or remove system accounts in accordance with organizational policies. Policies can include such information as account expiration dates or other factors that trigger the disabling of accounts. Organizations may choose to define access privileges or other attributes by account, type of account, or a combination of the two. Examples of other attributes required for authorizing access include restrictions on time of day, day of week, and point of origin. In defining other system account attributes, organizations consider system-related requirements and mission/business requirements. Failure to consider these factors could affect system availability.\nTemporary and emergency accounts are intended for short-term use. Organizations establish temporary accounts as part of normal account activation procedures when there is a need for short-term accounts without the demand for immediacy in account activation. Organizations establish emergency accounts in response to crisis situations and with the need for rapid account activation. Therefore, emergency account activation may bypass normal account authorization processes. Emergency and temporary accounts are not to be confused with infrequently used accounts, including local logon accounts used for special tasks or when network resources are unavailable (may also be known as accounts of last resort). Such accounts remain available and are not subject to automatic disabling or removal dates. Conditions for disabling or deactivating accounts include when shared/group, emergency, or temporary accounts are no longer required and when individuals are transferred or terminated. Changing shared/group authenticators when members leave the group is intended to ensure that former group members do not retain access to the shared or group account. Some types of system accounts may require specialized training.",
            "Related Controls": "AC-3, AC-5, AC-6, AC-17, AC-18, AC-20, AC-24, AU-2, AU-12, CM-5, IA-2, IA-4, IA-5, IA-8, MA-3, MA-5, PE-2, PL-4, PS-2, PS-4, PS-5, PS-7, PT-2, PT-3, SC-7, SC-12, SC-13, SC-37.",
        },
        {
            "Control Identifier": "AC-2(1)",
            "Control (or Control Enhancement) Name": "Account Management | Automated System Account Management",
            "Control Text": "Support the management of system accounts using [Assignment: organization-defined automated mechanisms].",
            "Discussion": "Automated system account management includes using automated mechanisms to create, enable, modify, disable, and remove accounts; notify account managers when an account is created, enabled, modified, disabled, or removed, or when users are terminated or transferred; monitor system account usage; and report atypical system account usage. Automated mechanisms can include internal system functions and email, telephonic, and text messaging notifications.",
            "Related Controls": "None.",
        },
        {
            "Control Identifier": "AC-2(2)",
            "Control (or Control Enhancement) Name": "Account Management | Automated Temporary and Emergency Account Management",
            "Control Text": "Automatically [Selection: remove; disable] temporary and emergency accounts after [Assignment: organization-defined time period for each type of account].",
            "Discussion": "Management of temporary and emergency accounts includes the removal or disabling of such accounts automatically after a predefined time period rather than at the convenience of the system administrator. Automatic removal or disabling of accounts provides a more consistent implementation.",
            "Related Controls": "None.",
        },
        {
            "Control Identifier": "AC-2(3)",
            "Control (or Control Enhancement) Name": "Account Management | Disable Accounts",
            "Control Text": "Disable accounts within [Assignment: organization-defined time period] when the accounts: \n(a) Have expired;\n(b) Are no longer associated with a user or individual;\n(c) Are in violation of organizational policy; or\n(d) Have been inactive for [Assignment: organization-defined time period].",
            "Discussion": "Disabling expired, inactive, or otherwise anomalous accounts supports the concepts of least privilege and least functionality which reduce the attack surface of the system.",
            "Related Controls": "None.",
        },
        {
            "Control Identifier": "SR-11",
            "Control (or Control Enhancement) Name": "Component Authenticity",
            "Control Text": "a. Develop and implement anti-counterfeit policy and procedures that include the means to detect and prevent counterfeit components from entering the system; and\nb. Report counterfeit system components to [Selection (one or more): source of counterfeit component; [Assignment: organization-defined external reporting organizations]; [Assignment: organization-defined personnel or roles]].",
            "Discussion": "Sources of counterfeit components include manufacturers, developers, vendors, and contractors. Anti-counterfeiting policies and procedures support tamper resistance and provide a level of protection against the introduction of malicious code. External reporting organizations include CISA.",
            "Related Controls": "PE-3, SA-4, SI-7, SR-9, SR-10.",
        },
        {
            "Control Identifier": "SR-11(1)",
            "Control (or Control Enhancement) Name": "Component Authenticity | Anti-counterfeit Training",
            "Control Text": "Train [Assignment: organization-defined personnel or roles] to detect counterfeit system components (including hardware, software, and firmware).",
            "Discussion": "None.",
            "Related Controls": "AT-3.",
        },
        {
            "Control Identifier": "SR-11(2)",
            "Control (or Control Enhancement) Name": "Component Authenticity | Configuration Control for Component Service and Repair",
            "Control Text": "Maintain configuration control over the following system components awaiting service or repair and serviced or repaired components awaiting return to service: [Assignment: organization-defined system components].",
            "Discussion": "None.",
            "Related Controls": "CM-3, MA-2, MA-4, SA-10.",
        },
        {
            "Control Identifier": "SR-11(3)",
            "Control (or Control Enhancement) Name": "Component Authenticity | Anti-counterfeit Scanning",
            "Control Text": "Scan for counterfeit system components [Assignment: organization-defined frequency].",
            "Discussion": "The type of component determines the type of scanning to be conducted (e.g., web application scanning if the component is a web application).",
            "Related Controls": "RA-5.",
        },
        {
            "Control Identifier": "SR-12",
            "Control (or Control Enhancement) Name": "Component Disposal",
            "Control Text": "Dispose of [Assignment: organization-defined data, documentation, tools, or system components] using the following techniques and methods: [Assignment: organization-defined techniques and methods].",
            "Discussion": "Data, documentation, tools, or system components can be disposed of at any time during the system development life cycle (not only in the disposal or retirement phase of the life cycle). For example, disposal can occur during research and development, design, prototyping, or operations/maintenance and include methods such as disk cleaning, removal of cryptographic keys, partial reuse of components. Opportunities for compromise during disposal affect physical and logical data, including system documentation in paper-based or digital files; shipping and delivery documentation; memory sticks with software code; or complete routers or servers that include permanent media, which contain sensitive or proprietary information. Additionally, proper disposal of system components helps to prevent such components from entering the gray market.",
            "Related Controls": "MP-6.",
        },
    ]
)


def test_detect():
    parser = NistSP80053v5Parser()

    assert parser.detect(test_data) is True


def test_detect_bad():
    parser = NistSP80053v5Parser()

    assert parser.detect("just some text") is False


def test_node_parse():
    parser = NistSP80053v5Parser()
    parser.parse_data(test_data, populate=False)

    node_df = parser.node_oriented_dfs["Control"]

    # there are 10 controls in the test data
    # plus 20 families defined by the parser
    assert len(node_df.index) == 10 + 20


def test_rel_parse():
    parser = NistSP80053v5Parser()
    parser.parse_data(test_data, populate=False)

    parents_df = parser.rel_input_dfs["CONTROL_HAS_PARENT_CONTROL"]["src_df"]

    assert len(parents_df.index) == 10


def test_populate(use_graph):
    parser = NistSP80053v5Parser()
    parser.parse_data(test_data, populate=True)

    ctrl_cypher = """MATCH (n:Control) RETURN COUNT(DISTINCT n)"""

    assert use_graph.evaluate_query_single(ctrl_cypher) == 10 + 20

    rel_cypher = """MATCH (:Control)-[r:CONTROL_HAS_PARENT_CONTROL]->(:Control) RETURN COUNT(DISTINCT r)"""

    assert use_graph.evaluate_query_single(rel_cypher) == 10


@pytest.mark.webtest
def test_parse_web():
    parser = NistSP80053v5Parser()
    parser.parse_url(
        "https://csrc.nist.gov/CSRC/media/Publications/sp/800-53/rev-5/final/documents/sp800-53r5-control-catalog.xlsx",
        populate=False,
    )

    node_df = parser.node_oriented_dfs["Control"]

    assert len(node_df.index) == 1189 + 20

    parents_df = parser.rel_input_dfs["CONTROL_HAS_PARENT_CONTROL"]["src_df"]

    assert len(parents_df.index) == 1189


@pytest.mark.slow
@pytest.mark.webtest
def test_populate_web(use_graph):
    parser = NistSP80053v5Parser()
    parser.parse_url(
        "https://csrc.nist.gov/CSRC/media/Publications/sp/800-53/rev-5/final/documents/sp800-53r5-control-catalog.xlsx",
        populate=True,
    )

    ctrl_cypher = """MATCH (n:Control) RETURN COUNT(DISTINCT n)"""

    assert use_graph.evaluate_query_single(ctrl_cypher) == 1189 + 20

    rel_cypher = """MATCH (:Control)-[r:CONTROL_HAS_PARENT_CONTROL]->(:Control) RETURN COUNT(DISTINCT r)"""

    assert use_graph.evaluate_query_single(rel_cypher) == 1189


@pytest.mark.slow
@pytest.mark.webtest
def test_populate_file(use_graph, tmp_path):
    tmp_file = tmp_path / "sp80053.4.xlsx"

    url = "https://csrc.nist.gov/CSRC/media/Publications/sp/800-53/rev-5/final/documents/sp800-53r5-control-catalog.xlsx"
    response = requests.get(url)

    with open(tmp_file, "wb") as file:
        file.write(response.content)

    parser = NistSP80053v5Parser()
    parser.parse_file(str(tmp_file), populate=True)

    ctrl_cypher = """MATCH (n:Control) RETURN COUNT(DISTINCT n)"""

    assert use_graph.evaluate_query_single(ctrl_cypher) == 1189 + 20

    rel_cypher = """MATCH (:Control)-[r:CONTROL_HAS_PARENT_CONTROL]->(:Control) RETURN COUNT(DISTINCT r)"""

    assert use_graph.evaluate_query_single(rel_cypher) == 1189
