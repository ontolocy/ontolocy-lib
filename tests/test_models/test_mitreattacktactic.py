from ontolocy import MitreAttackTactic

from pydantic import ValidationError
import pytest

stix_dict = {
    "x_mitre_domains": ["enterprise-attack"],
    "object_marking_refs": ["marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"],
    "id": "x-mitre-tactic--2558fd61-8c75-4730-94c4-11926db2a263",
    "type": "x-mitre-tactic",
    "created": "2018-10-17T00:14:20.652Z",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "external_references": [
        {
            "external_id": "TA0006",
            "url": "https://attack.mitre.org/tactics/TA0006",
            "source_name": "mitre-attack",
        }
    ],
    "modified": "2022-04-25T14:00:00.188Z",
    "name": "Credential Access",
    "description": "The adversary is trying to steal account names and passwords.\n\nCredential Access consists of techniques for stealing credentials like account names and passwords. Techniques used to get credentials include keylogging or credential dumping. Using legitimate credentials can give adversaries access to systems, make them harder to detect, and provide the opportunity to create more accounts to help achieve their goals.",
    "x_mitre_version": "1.0",
    "x_mitre_attack_spec_version": "2.1.0",
    "x_mitre_modified_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "x_mitre_shortname": "credential-access",
    "spec_version": "2.1",
}


def test_tactic():

    tactic = MitreAttackTactic(
        stix_id=stix_dict["id"],
        stix_type=stix_dict["type"],
        stix_created=stix_dict["created"],
        stix_modified=stix_dict["modified"],
        attack_id=stix_dict["external_references"][0]["external_id"],
        attack_spec_version=stix_dict["x_mitre_attack_spec_version"],
        attack_shortname=stix_dict["x_mitre_shortname"],
        attack_version=stix_dict["x_mitre_version"],
        ref_url=stix_dict["external_references"][0]["url"],
        name=stix_dict["name"],
        description=stix_dict["description"],
    )

    assert tactic.get_pp() == "x-mitre-tactic--2558fd61-8c75-4730-94c4-11926db2a263"


def test_tactic_bad():

    with pytest.raises(ValidationError):
        MitreAttackTactic(
            stix_id=stix_dict["id"],
            stix_type=stix_dict["type"],
            stix_created=stix_dict["created"],
            stix_modified=stix_dict["modified"],
            attack_id="BAD12345",
            attack_spec_version=stix_dict["x_mitre_attack_spec_version"],
            attack_shortname=stix_dict["x_mitre_shortname"],
            attack_version=stix_dict["x_mitre_version"],
            ref_url=stix_dict["external_references"][0]["url"],
            name=stix_dict["name"],
            description=stix_dict["description"],
        )
