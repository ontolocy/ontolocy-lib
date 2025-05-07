import pytest

from ontolocy.tools import CTIDAttackMappingsParser

test_data = {
    "metadata": {
        "mapping_version": "",
        "technology_domain": "enterprise",
        "attack_version": "16.1",
        "mapping_framework": "nist_800_53",
        "mapping_framework_version": "rev5",
        "author": None,
        "contact": None,
        "organization": None,
        "creation_date": "01/13/2022",
        "last_update": "04/16/2025",
        "mapping_types": {"mitigates": {"name": "mitigates", "description": ""}},
        "capability_groups": {
            "AC": "Access Control",
            "CA": "Security Assessment and Authorization",
            "CM": "Configuration Management",
            "SC": "System and Communications Protection",
            "SI": "System and Information Integrity",
            "CP": "Contingency Planning",
            "IA": "Identification and Authentication",
            "SA": "System and Services Acquisition",
            "RA": "Risk Assessment",
            "MP": "Media Protection",
            "SR": "Supply Chain Risk Management",
        },
    },
    "mapping_objects": [
        {
            "capability_id": None,
            "capability_group": None,
            "capability_description": None,
            "mapping_type": None,
            "attack_object_id": "T1496.002",
            "attack_object_name": "Bandwidth Hijacking",
            "comments": "no mitiigations in att&ck",
            "references": [],
            "status": "non_mappable",
        },
        {
            "capability_id": "CM-03",
            "capability_description": "Configuration Change Control",
            "mapping_type": "mitigates",
            "attack_object_id": "T1666",
            "attack_object_name": "Modify Cloud Resource Hierarchy",
            "capability_group": "CM",
            "comments": "Monitoring and reviewing changes to the configuration of the IaaS environment (in this case, the cloud resource hierarchy) allows for the detection and reversal of unauthorized changes to prevent exploitation.",
            "references": [],
            "status": "complete",
        },
        {
            "capability_id": "AC-02",
            "capability_description": "Account Management",
            "mapping_type": "mitigates",
            "attack_object_id": "T1556.009",
            "attack_object_name": "Conditional Access Policies",
            "capability_group": "AC",
            "comments": "Control AC-2 (Account Management) contains provisions for the monitoring of accounts for unusual activity and atypical usage as part of a dynamic account management approach. By monitoring these accounts, the system may be able to detect unauthorized changes to the accounts and take the necessary steps, either automatically or by alerting personnel, to remedy and mitigate the issue.",
            "references": [],
            "status": "complete",
        },
        {
            "capability_id": "SC-05",
            "capability_description": "Denial-of-service Protection",
            "mapping_type": "mitigates",
            "attack_object_id": "T1496.003",
            "attack_object_name": "SMS Pumping",
            "capability_group": "SC",
            "references": [],
            "status": "complete",
        },
        {
            "capability_id": "AC-06",
            "capability_description": "Least Privilege",
            "mapping_type": "mitigates",
            "attack_object_id": "T1110",
            "attack_object_name": "Brute Force",
            "capability_group": "AC",
            "references": [],
            "status": "complete",
        },
    ],
}


def test_detect():
    parser = CTIDAttackMappingsParser()

    assert parser.detect(test_data) is True


def test_detect_bad():
    parser = CTIDAttackMappingsParser()

    assert parser.detect("not good test data") is False


def test_rel_parse():
    parser = CTIDAttackMappingsParser()
    parser.parse_data(test_data, populate=False)

    rel_df = parser.rel_input_dfs["CONTROL_MITIGATES_ATTACK_TECHNIQUE"]["src_df"]

    assert len(rel_df.index) == 4


@pytest.mark.webtest
def test_rel_parse_rev4():
    parser = CTIDAttackMappingsParser()
    parser.parse_url(
        "https://github.com/center-for-threat-informed-defense/mappings-explorer/raw/refs/heads/main/mappings/nist_800_53/attack-14.1/nist_800_53-rev4/enterprise/nist_800_53-rev4_attack-14.1-enterprise.json",
        populate=False,
    )

    rel_df = parser.rel_input_dfs["CONTROL_MITIGATES_ATTACK_TECHNIQUE"]["src_df"]

    assert len(rel_df.index) == 4972


@pytest.mark.webtest
def test_rel_parse_rev5():
    parser = CTIDAttackMappingsParser()
    parser.parse_url(
        "https://raw.githubusercontent.com/center-for-threat-informed-defense/mappings-explorer/refs/heads/main/mappings/nist_800_53/attack-16.1/nist_800_53-rev5/enterprise/nist_800_53-rev5_attack-16.1-enterprise.json",
        populate=False,
    )

    rel_df = parser.rel_input_dfs["CONTROL_MITIGATES_ATTACK_TECHNIQUE"]["src_df"]

    assert len(rel_df.index) == 5314
