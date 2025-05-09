from io import StringIO

import pandas as pd

from ontolocy import Control, ControlHasParentControl

from .ontolocy_parser import OntolocyParser


class NistSP80053v4Parser(OntolocyParser):
    """Parser for NIST SP 800-53 Rev. 4 data.

    This parser is designed to parse NIST SP 800-53 Rev. 4 controls in CSV format.

    https://csrc.nist.gov/csrc/media/Projects/risk-management/800-53%20Downloads/800-53r4/800-53-rev4-controls.csv
    """

    node_types = [Control]
    rel_types = [ControlHasParentControl]

    def _detect(self, input_data) -> bool:
        print(input_data)

        columns = [
            "FAMILY",
            "NAME",
            "TITLE",
            "PRIORITY",
            "BASELINE-IMPACT",
            "DESCRIPTION",
            "SUPPLEMENTAL GUIDANCE",
            "RELATED",
        ]

        try:
            input_columns = input_data.columns.to_list()
        except AttributeError:
            return False

        if input_columns == columns:
            return True

        return False

    def _load_data(self, raw_data) -> pd.DataFrame:
        return pd.read_csv(StringIO(raw_data))

    def _parse(self, input_data, private_namespace=None) -> tuple:
        FRAMEWORK = "NIST SP 800-53"
        FRAMEWORK_VERSION = "Rev. 4"
        FRAMEWORK_URL = "https://doi.org/10.6028/NIST.SP.800-53r4"

        node_dfs = {}
        rel_dfs = {}

        df = input_data.rename(
            columns={
                "NAME": "control_id",
                "DESCRIPTION": "description",
                "SUPPLEMENTAL GUIDANCE": "context",
            },
        ).copy()

        df["name"] = df["control_id"]

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
            "RA": "Risk Assessment",
            "SA": "System and Services Acquisition",
            "SC": "System and Communications Protection",
            "SI": "System and Information Integrity",
        }

        families_df = pd.DataFrame()
        families_df["control_id"] = families.keys()
        families_df["name"] = families.values()

        families_df["framework"] = FRAMEWORK
        families_df["framework_level"] = "Family"
        families_df["framework_version"] = FRAMEWORK_VERSION
        families_df["url_reference"] = FRAMEWORK_URL

        families_df["unique_id"] = families_df["control_id"].map(
            lambda x: f"nist.sp80053.rev4.{x}"
        )

        # Controls

        control_df = df[["control_id", "name", "description", "context"]].copy()

        control_df["framework"] = FRAMEWORK
        control_df["framework_level"] = "Control"
        control_df["framework_version"] = FRAMEWORK_VERSION
        control_df["url_reference"] = FRAMEWORK_URL

        control_df["unique_id"] = control_df["control_id"].map(
            lambda x: f"nist.sp80053.rev4.{x}"
        )

        all_controls_df = pd.concat([families_df, control_df])

        node_dfs[Control.__primarylabel__] = all_controls_df.copy()

        #
        # Relationships
        #

        # ControlHasParentControl

        control_to_family_df = pd.DataFrame()
        control_to_family_df["source"] = control_df["unique_id"]
        control_to_family_df["target"] = control_df["control_id"].map(
            lambda x: f"nist.sp80053.rev4.{x[0:2]}"
        )
        control_to_family_df["url_reference"] = FRAMEWORK_URL

        rel_dfs[ControlHasParentControl.__relationshiptype__] = {
            "src_df": control_to_family_df[["source"]].copy(),
            "tgt_df": control_to_family_df[["target"]].copy(),
            "props_df": control_to_family_df[["url_reference"]].copy(),
        }

        # Related Controls

        return node_dfs, rel_dfs
