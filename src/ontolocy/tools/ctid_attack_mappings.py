import json

import pandas as pd

from ontolocy import ControlMitigatesAttackTechnique

from .ontolocy_parser import OntolocyParser


class CTIDAttackMappingsParser(OntolocyParser):
    """Parser for MITRE Centre for Threat Informed Defense ATT&CK mappings data.

    https://github.com/center-for-threat-informed-defense/mappings-explorer
    """

    node_types = []
    rel_types = [ControlMitigatesAttackTechnique]

    relationship_kwargs = {
        ControlMitigatesAttackTechnique.__relationshiptype__: {
            "target_prop": "attack_id"
        }
    }

    def _detect(self, input_data) -> bool:
        try:
            metadata = input_data.get("metadata")

        except AttributeError:
            return False

        if "mapping_framework" in metadata:
            return True

        else:
            return False

    def _load_data(self, raw_data):
        return json.loads(raw_data)

    def _parse(self, input_data, private_namespace=None) -> tuple:
        node_dfs = {}
        rel_dfs = {}

        namespaces = {
            "nist_800_53": {"rev4": "nist.sp80053.rev4.", "rev5": "nist.sp80053.rev5."}
        }

        framework = input_data["metadata"]["mapping_framework"]
        framework_version = input_data["metadata"]["mapping_framework_version"]

        prefix = namespaces[framework][framework_version]

        URL_REF = (
            "https://github.com/center-for-threat-informed-defense/mappings-explorer"
        )

        mappings = input_data["mapping_objects"]

        mapping_df = pd.DataFrame.from_records(mappings)

        mapping_df["source"] = prefix + mapping_df["capability_id"]
        mapping_df["target"] = mapping_df["attack_object_id"]
        mapping_df["url_reference"] = URL_REF

        #
        # Relationships
        #

        # Controls to ATT&&CK techniques

        protect_df = mapping_df[
            mapping_df["mapping_type"].isin(["protects", "mitigates"])
        ][["source", "target", "url_reference"]].copy()

        rel_dfs[ControlMitigatesAttackTechnique.__relationshiptype__] = {
            "src_df": protect_df[["source"]].copy(),
            "tgt_df": protect_df[["target"]].copy(),
            "props_df": protect_df[["url_reference"]].copy(),
        }

        return node_dfs, rel_dfs
