from io import BytesIO

import pandas as pd
import requests

from ontolocy import Control, ControlHasParentControl

from .ontolocy_parser import OntolocyParser


class NistSP80053v5Parser(OntolocyParser):
    """Parser for NIST SP 800-53 Rev. 5 data.

    This parser is designed to parse NIST SP 800-53 Rev. 5
    'Control Catalog Spreadsheet' data in xlsx format.

    https://csrc.nist.gov/CSRC/media/Publications/sp/800-53/rev-5/final/documents/sp800-53r5-control-catalog.xlsx
    """

    node_types = [Control]
    rel_types = [ControlHasParentControl]

    def _detect(self, input_data) -> bool:
        columns = [
            "Control Identifier",
            "Control (or Control Enhancement) Name",
            "Control Text",
            "Discussion",
            "Related Controls",
        ]

        try:
            input_columns = input_data.columns.to_list()
        except AttributeError:
            return False

        if input_columns == columns:
            return True

        return False

    def _load_data(self, raw_data):
        return pd.read_excel(BytesIO(raw_data))

    def _load_file(self, file_path):
        with open(file_path, "rb") as f:  # type: ignore [arg-type]
            data = f.read()

        return data

    def _load_url(self, url):
        response = requests.get(url)

        return response.content

    def _parse(self, input_data: pd.DataFrame, private_namespace=None) -> tuple:
        FRAMEWORK = "NIST SP 800-53"
        FRAMEWORK_VERSION = "Rev. 5"
        FRAMEWORK_URL = "https://doi.org/10.6028/NIST.SP.800-53r5"

        node_dfs = {}
        rel_dfs = {}

        df = input_data.rename(
            columns={
                "Control Identifier": "control_id",
                "Control (or Control Enhancement) Name": "name",
                "Control Text": "description",
                "Discussion": "context",
                "Related Controls": "raw_related_controls",
            },
        ).copy()

        #
        # Nodes
        #

        # Families

        families = {
            "AC": "Access Control",
            "AU": "Audit and Accountability",
            "AT": "Awareness and Training",
            "CA": "Security Assessment and Authorization",
            "CM": "Configuration Management",
            "CP": "Contingency Planning",
            "IA": "Identification and Authentication",
            "IR": "Incident Response",
            "MA": "Maintenance",
            "MP": "Media Protection",
            "PE": "Physical and Environmental Protection",
            "PM": "Program Management",
            "PL": "Planning",
            "PS": "Personnel Security",
            "PT": "Personally Identifiable Information Processing and Transparency",
            "RA": "Risk Assessment",
            "SA": "System and Services Acquisition",
            "SC": "System and Communications Protection",
            "SI": "System and Information Integrity",
            "SR": "Supply Chain Risk Management",
        }

        families_df = pd.DataFrame()
        families_df["control_id"] = families.keys()
        families_df["name"] = families.values()

        families_df["framework"] = FRAMEWORK
        families_df["framework_level"] = "Family"
        families_df["framework_version"] = FRAMEWORK_VERSION
        families_df["url_reference"] = FRAMEWORK_URL

        families_df["unique_id"] = families_df["control_id"].map(
            lambda x: f"nist.sp80053.rev5.{x}"
        )

        # Controls

        control_df = df[["control_id", "name", "description", "context"]]

        control_df["framework"] = FRAMEWORK
        control_df["framework_level"] = "Control"
        control_df["framework_version"] = FRAMEWORK_VERSION
        control_df["url_reference"] = FRAMEWORK_URL

        control_df["unique_id"] = control_df["control_id"].map(
            lambda x: f"nist.sp80053.rev5.{x}"
        )

        all_controls_df = pd.concat([families_df, control_df])

        node_dfs[Control.__primarylabel__] = all_controls_df.copy()

        #
        # Relationships
        #

        # Control to Family

        control_to_family_df = pd.DataFrame()
        control_to_family_df["source"] = control_df["unique_id"]
        control_to_family_df["target"] = control_df["control_id"].map(
            lambda x: f"nist.sp80053.rev5.{x[0:2]}"
        )
        control_to_family_df["url_reference"] = FRAMEWORK_URL

        rel_dfs[ControlHasParentControl.__relationshiptype__] = {
            "src_df": control_to_family_df[["source"]].copy(),
            "tgt_df": control_to_family_df[["target"]].copy(),
            "props_df": control_to_family_df[["url_reference"]].copy(),
        }

        # Related Controls

        return node_dfs, rel_dfs
