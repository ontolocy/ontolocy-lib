import pandas as pd

from ontolocy import (
    CAPECPattern,
    CAPECPatternMapsToAttackTechnique,
    MitreAttackTechnique,
)

stix_dict = {
    "x_mitre_platforms": ["PRE"],
    "x_mitre_domains": ["enterprise-attack"],
    "x_mitre_contributors": [
        "Philip Winther",
        "Sebastian Salla, McAfee",
        "Robert Simmons, @MalwareUtkonos",
    ],
    "object_marking_refs": ["marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"],
    "id": "attack-pattern--2d3f5b3c-54ca-4f4d-bb1f-849346d31230",
    "type": "attack-pattern",
    "created": "2020-10-02T17:09:50.723Z",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "external_references": [
        {
            "source_name": "mitre-attack",
            "external_id": "T1598.003",
            "url": "https://attack.mitre.org/techniques/T1598/003",
        },
        {
            "source_name": "TrendMictro Phishing",
            "url": "https://www.trendmicro.com/en_us/research/20/i/tricky-forms-of-phishing.html",
            "description": "Babon, P. (2020, September 3). Tricky 'Forms' of Phishing. Retrieved October 20, 2020.",
        },
        {
            "source_name": "PCMag FakeLogin",
            "url": "https://www.pcmag.com/news/hackers-try-to-phish-united-nations-staffers-with-fake-login-pages",
            "description": "Kan, M. (2019, October 24). Hackers Try to Phish United Nations Staffers With Fake Login Pages. Retrieved October 20, 2020.",
        },
        {
            "source_name": "Microsoft Anti Spoofing",
            "url": "https://docs.microsoft.com/en-us/microsoft-365/security/office-365-security/anti-spoofing-protection?view=o365-worldwide",
            "description": "Microsoft. (2020, October 13). Anti-spoofing protection in EOP. Retrieved October 19, 2020.",
        },
        {
            "source_name": "ACSC Email Spoofing",
            "url": "https://www.cyber.gov.au/sites/default/files/2019-03/spoof_email_sender_policy_framework.pdf",
            "description": "Australian Cyber Security Centre. (2012, December). Mitigating Spoofed Emails Using Sender Policy Framework. Retrieved October 19, 2020.",
        },
    ],
    "modified": "2022-05-11T14:00:00.188Z",
    "name": "Spearphishing Link",
    "description": "Adversaries may send spearphishing messages with a malicious link to elicit sensitive information that can be used during targeting. Spearphishing for information is an attempt to trick targets into divulging information, frequently credentials or other actionable information. Spearphishing for information frequently involves social engineering techniques, such as posing as a source with a reason to collect information (ex: [Establish Accounts](https://attack.mitre.org/techniques/T1585) or [Compromise Accounts](https://attack.mitre.org/techniques/T1586)) and/or sending multiple, seemingly urgent messages.\n\nAll forms of spearphishing are electronically delivered social engineering targeted at a specific individual, company, or industry. In this scenario, the malicious emails contain links generally accompanied by social engineering text to coax the user to actively click or copy and paste a URL into a browser.(Citation: TrendMictro Phishing)(Citation: PCMag FakeLogin) The given website may closely resemble a legitimate site in appearance and have a URL containing elements from the real site. From the fake website, information is gathered in web forms and sent to the adversary. Adversaries may also use information from previous reconnaissance efforts (ex: [Search Open Websites/Domains](https://attack.mitre.org/techniques/T1593) or [Search Victim-Owned Websites](https://attack.mitre.org/techniques/T1594)) to craft persuasive and believable lures.",
    "kill_chain_phases": [
        {"kill_chain_name": "mitre-attack", "phase_name": "reconnaissance"}
    ],
    "x_mitre_detection": "Monitor for suspicious email activity, such as numerous accounts receiving messages from a single unusual/unknown sender. Filtering based on DKIM+SPF or header analysis can help detect when the email sender is spoofed.(Citation: Microsoft Anti Spoofing)(Citation: ACSC Email Spoofing)\n\nMonitor for references to uncategorized or known-bad sites. URL inspection within email (including expanding shortened links) can also help detect links leading to known malicious sites.",
    "x_mitre_is_subtechnique": True,
    "x_mitre_version": "1.2",
    "x_mitre_modified_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "x_mitre_data_sources": [
        "Network Traffic: Network Traffic Content",
        "Network Traffic: Network Traffic Flow",
        "Application Log: Application Log Content",
    ],
    "spec_version": "2.1",
    "x_mitre_attack_spec_version": "2.1.0",
}


def test_capec():
    capec = CAPECPattern(
        capec_id=1001,
        description="hello world",
        name="foo bar",
        likelihood_of_attack="High",
        typical_severity="Low",
    )

    assert capec.get_pp() == 1001


def test_capec_maps_to_attack(use_graph):
    capec = CAPECPattern(
        capec_id=1001,
        description="hello world",
        name="foo bar",
        likelihood_of_attack="High",
        typical_severity="Low",
    )

    capec.merge()

    technique = MitreAttackTechnique(
        stix_id=stix_dict["id"],
        stix_type=stix_dict["type"],
        stix_created=stix_dict["created"],
        stix_modified=stix_dict["modified"],
        attack_id=stix_dict["external_references"][0]["external_id"],
        attack_spec_version=stix_dict["x_mitre_attack_spec_version"],
        attack_subtechnique=stix_dict["x_mitre_is_subtechnique"],
        attack_version=stix_dict["x_mitre_version"],
        ref_url=stix_dict["external_references"][0]["url"],
        name=stix_dict["name"],
        description=stix_dict["description"],
    )

    technique.merge()

    df = pd.DataFrame.from_records(
        [{"source": capec.get_pp(), "target": technique.attack_id}]
    )

    CAPECPatternMapsToAttackTechnique.ingest_df(df, target_prop="attack_id")

    cypher = """
    MATCH (capec:CAPECPattern)-[r:CAPEC_PATTERN_MAPS_TO_ATTACK_TECHNIQUE]->(:MitreAttackTechnique)
    WHERE capec.capec_id = $capec_id
    RETURN COUNT(DISTINCT r)
    """

    params = {"capec_id": capec.get_pp()}

    result = use_graph.evaluate_query_single(cypher, params)

    assert result == 1
