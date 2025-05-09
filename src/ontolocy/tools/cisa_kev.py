from io import StringIO

import pandas as pd

from ontolocy import CVE, Organisation, OrganisationReportedExploitationOfCVE

from .ontolocy_parser import OntolocyParser


class CisaKevParser(OntolocyParser):
    """Parser for CISA's Known Exploited Vulnerabilities data.

    https://www.cisa.gov/known-exploited-vulnerabilities-catalog

    It expects the CSV file available at:

    https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv

    """

    node_types = [CVE, Organisation]
    rel_types = [OrganisationReportedExploitationOfCVE]

    def _detect(self, input_data) -> bool:
        columns = [
            "cveID",
            "vendorProject",
            "product",
            "vulnerabilityName",
            "dateAdded",
            "shortDescription",
            "requiredAction",
            "dueDate",
            "knownRansomwareCampaignUse",
            "notes",
            "cwes",
        ]

        try:
            input_columns = list(input_data.columns)

        except AttributeError:
            # If the input is not a DataFrame, we can't detect it
            # When loading from a file, or URL, _load_data should convert it to a DataFrame
            return False

        if input_columns == columns:
            return True

        return False

    def _load_data(self, raw_data):
        return pd.read_csv(StringIO(raw_data))

    def _parse(self, input_data, private_namespace=None) -> tuple:
        node_dfs = {}
        rel_dfs = {}

        df = input_data.rename(
            columns={
                "cveID": "cve_id",
                "shortDescription": "description",
                "dateAdded": "reported_date",
                "requiredAction": "required_action",
            },
        ).copy()

        #
        # Nodes
        #

        # CVEs

        node_dfs[CVE.__primarylabel__] = df[["cve_id"]]

        # Reporting Organization

        ORGANISATION = "US Cyber Security & Infrastructure Agency"

        node_dfs[Organisation.__primarylabel__] = pd.DataFrame({"name": [ORGANISATION]})

        #
        # Relationships
        #

        # OrganisationReportedExploitationOfCVE

        org_rels_df = df[
            ["cve_id", "reported_date", "description", "required_action"]
        ].rename(columns={"cve_id": "target"})
        org_rels_df["source"] = ORGANISATION
        org_rels_df["url_reference"] = (
            "https://www.cisa.gov/known-exploited-vulnerabilities-catalog"
        )

        rel_dfs[OrganisationReportedExploitationOfCVE.__relationshiptype__] = {
            "src_df": org_rels_df[["source"]].copy(),
            "tgt_df": org_rels_df[["target"]].copy(),
            "props_df": org_rels_df[
                ["url_reference", "reported_date", "description", "required_action"]
            ].copy(),
        }

        return node_dfs, rel_dfs
