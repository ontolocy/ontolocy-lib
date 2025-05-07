import json
import os

import pandas as pd
import requests

from ontolocy import (
    CPE,
    CVE,
    CVERelatesToCPE,
    CVERelatesToCWE,
    Organisation,
    OrganisationAssignedCVSSToCVE,
)

from .ontolocy_enricher import OntolocyClient, OntolocyEnricher, SeedTypeEnum
from .ontolocy_parser import OntolocyParser


class NVDCVEParser(OntolocyParser):
    node_types = [
        CVE,
        CPE,
        Organisation,
    ]

    rel_types = [
        OrganisationAssignedCVSSToCVE,
        CVERelatesToCPE,
        CVERelatesToCWE,
    ]

    def _load_data(self, raw_data):
        return json.loads(raw_data)

    def _detect(self, input_data) -> bool:
        try:
            input_data.get("format")
        except AttributeError:
            return False

        if (
            input_data.get("format") == "NVD_CVE"
            and len(input_data.get("vulnerabilities", [])) > 0
        ):
            return True
        else:
            return False

    def _parse(self, input_data, private_namespace=None) -> tuple:
        node_dfs = {}
        rel_dfs = {}

        try:
            data = json.loads(input_data)
        except (TypeError, json.JSONDecodeError):
            data = input_data

        cvss_org_name = "NIST National Vulnerability Database"

        orgs = [{"name": cvss_org_name}]
        cves = []
        cpes = []
        cve_to_cwe = []
        cvss_rels = []
        cve_to_cpe = []

        # process the raw data

        for vuln_entry in data.get("vulnerabilities", []):
            cve_entry = vuln_entry.get("cve")
            if not cve_entry:
                continue
            cve_id = cve_entry["id"]
            cve = {
                "cve_id": cve_id,
                "published_date": cve_entry["published"],
            }

            for description in cve_entry["descriptions"]:
                if description.get("lang") == "en":
                    cve["description"] = description["value"]
                    break

            cves.append(cve)

            for cwe in cve_entry.get("weaknesses", []):
                for description in cwe["description"]:
                    if description["value"].startswith("CWE-"):
                        cve_to_cwe.append(
                            {
                                "source": cve_id,
                                "target": int(description["value"].replace("CWE-", "")),
                            }
                        )

            for cvss_entry in (
                cve_entry.get("metrics", {}).get("cvssMetricV31", [])
            ) + cve_entry.get("metrics", {}).get("cvssMetricV30", []):
                cvss_rels.append(
                    {
                        "source": cvss_org_name,
                        "target": cve_id,
                        "version": cvss_entry["cvssData"]["version"],
                        "vector_string": cvss_entry["cvssData"]["vectorString"],
                        "attack_vector": cvss_entry["cvssData"]["attackVector"],
                        "attack_complexity": cvss_entry["cvssData"]["attackComplexity"],
                        "privileges_required": cvss_entry["cvssData"][
                            "privilegesRequired"
                        ],
                        "user_interaction": cvss_entry["cvssData"]["userInteraction"],
                        "scope": cvss_entry["cvssData"]["scope"],
                        "confidentiality_impact": cvss_entry["cvssData"][
                            "confidentialityImpact"
                        ],
                        "integrity_impact": cvss_entry["cvssData"]["integrityImpact"],
                        "availability_impact": cvss_entry["cvssData"][
                            "availabilityImpact"
                        ],
                        "base_score": cvss_entry["cvssData"]["baseScore"],
                        "base_severity": cvss_entry["cvssData"]["baseSeverity"],
                        "exploitability_score": cvss_entry["exploitabilityScore"],
                        "impact_score": cvss_entry["impactScore"],
                    }
                )

            for config_entry in cve_entry.get("configurations", []):
                for node in config_entry.get("nodes", []):
                    for cpe_match in node.get("cpeMatch", []):
                        if cpe_match.get("vulnerable") is True:
                            full_cpe_id = cpe_match.get("criteria")

                            # neontology CPEs are truncated to product
                            product_cpe = CPE(cpe=full_cpe_id).cpe

                            cpes.append({"cpe": product_cpe})
                            cve_to_cpe.append(
                                {
                                    "source": cve_id,
                                    "target": product_cpe,
                                    "cpe": full_cpe_id,
                                }
                            )

        # now create the data frames

        #
        # Nodes
        #

        node_dfs[CVE.__primarylabel__] = pd.DataFrame(cves)

        node_dfs[CPE.__primarylabel__] = pd.DataFrame(cpes)

        node_dfs[Organisation.__primarylabel__] = pd.DataFrame(orgs)

        #
        # Relationships
        #

        cve_to_cpe_df = pd.DataFrame(cve_to_cpe)

        rel_dfs[CVERelatesToCPE.__relationshiptype__] = {
            "src_df": cve_to_cpe_df[["source"]].copy(),
            "tgt_df": cve_to_cpe_df[["target"]].copy(),
            "props_df": cve_to_cpe_df.drop(columns=["source", "target"]).copy(),
        }

        rel_dfs[CVERelatesToCWE.__relationshiptype__] = {
            "src_df": pd.DataFrame(cve_to_cwe)[["source"]],
            "tgt_df": pd.DataFrame(cve_to_cwe)[["target"]],
        }

        cvss_df = pd.DataFrame(cvss_rels)

        rel_dfs[OrganisationAssignedCVSSToCVE.__relationshiptype__] = {
            "src_df": cvss_df[["source"]].copy(),
            "tgt_df": cvss_df[["target"]].copy(),
            "props_df": cvss_df.drop(columns=["source", "target"]).copy(),
        }

        return node_dfs, rel_dfs


class NVDCVEOntolocyClient(OntolocyClient):
    """Lightweight client for NVD CVE data.

    Takes query parameters (https://nvd.nist.gov/developers/vulnerabilities) and populates the graph with CVE results.

    Query parameters are passed as a dictionary, using naming defined in the NVD API documentation.
    """

    def __init__(self):
        super().__init__()

        self.parser = NVDCVEParser()

        self.nvd_api_key = os.getenv("ONTOLOCY_NVD_KEY")

    def _query(self, query):
        api_endpoint = "https://services.nvd.nist.gov/rest/json/cves/2.0"

        if self.nvd_api_key:
            headers = {"apiKey": self.nvd_api_key}
        else:
            headers = {}

        response = requests.get(api_endpoint, headers=headers, params=query)

        # raise an exception if the request was unsuccessful
        response.raise_for_status()

        return response.json()


class NVDCVEEnricher(OntolocyEnricher):
    seed_type = SeedTypeEnum.CVE

    def __init__(self):
        super().__init__()
        self.client = NVDCVEOntolocyClient()

    def _generate_single_query(self, seed):
        return {"cveId": seed}
