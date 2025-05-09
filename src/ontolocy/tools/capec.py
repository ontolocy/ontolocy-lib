import pandas as pd
import xmltodict

from ontolocy import (
    CAPECPattern,
    CAPECPatternMapsToAttackTechnique,
    CAPECPatternRelatesToCWE,
)

from .ontolocy_parser import OntolocyParser


class CapecParser(OntolocyParser):
    """Parser for MITRE's Common Attack Pattern Enumerations and Classifications

    https://capec.mitre.org/

    Expects an XML file. For example:

    https://capec.mitre.org/data/xml/capec_latest.xml

    """

    node_types = [CAPECPattern]
    rel_types = [
        CAPECPatternMapsToAttackTechnique,
        CAPECPatternRelatesToCWE,
    ]

    relationship_kwargs = {
        CAPECPatternMapsToAttackTechnique.__relationshiptype__: {
            "target_prop": "attack_id"
        }
    }

    def _detect(self, input_data) -> bool:
        try:
            catalogue_name = input_data.get("Attack_Pattern_Catalog", {}).get("@Name")
        except AttributeError:
            return False

        if catalogue_name == "CAPEC":
            return True

        else:
            return False

    def _process_description(self, input):
        try:
            xhtml = list(input.values())

        except AttributeError:
            return input

        entry_strings = []

        for entry in xhtml:
            if isinstance(entry, list):
                entry_strings += [self._process_description(x) for x in entry]

            else:
                entry_strings.append(self._process_description(entry))

        return " ".join(entry_strings)

    def _load_data(self, raw_data):
        data = xmltodict.parse(
            str(raw_data), force_list={"Related_Weakness", "Taxonomy_Mapping"}
        )

        return data

    def _parse(self, input_data, private_namespace=None) -> tuple:
        node_dfs = {}
        rel_dfs = {}

        capec_catalogue = input_data.get("Attack_Pattern_Catalog", [])

        records = [
            {
                "capec_id": int(x["@ID"]),
                "description": x["Description"],
                "name": x["@Name"],
                "likelihood_of_attack": x.get("Likelihood_Of_Attack"),
                "typical_severity": x.get("Typical_Severity"),
                "related_weaknesses": x.get("Related_Weaknesses", {}).get(
                    "Related_Weakness", []
                ),
                "taxonomy_mappings": x.get("Taxonomy_Mappings", {}).get(
                    "Taxonomy_Mapping", []
                ),
                "status": x.get("@Status"),
            }
            for x in capec_catalogue["Attack_Patterns"]["Attack_Pattern"]
        ]

        # tidy up records
        for idx, record in enumerate(records):
            new_record = record

            new_record["description"] = self._process_description(record["description"])

            # pull out MITRE ATT&CK techniques
            new_record["attack_techniques"] = [
                f"T{x['Entry_ID']}"
                for x in record["taxonomy_mappings"]
                if x["@Taxonomy_Name"] == "ATTACK"
            ]

            # pull out CWE IDs
            new_record["cwes"] = [
                int(x["@CWE_ID"]) for x in record["related_weaknesses"]
            ]

            records[idx] = new_record

        full_df = pd.DataFrame.from_records(records)

        #
        # Nodes
        #

        # CAPEC

        capec_df = full_df[
            [
                "capec_id",
                "description",
                "name",
                "likelihood_of_attack",
                "typical_severity",
                "status",
            ]
        ].copy()

        node_dfs[CAPECPattern.__primarylabel__] = capec_df

        #
        # Relationships
        #

        # CAPECPatternMapsToAttackTechnique

        attack_df = full_df.explode("attack_techniques", ignore_index=True).copy()
        attack_df = attack_df.loc[attack_df["attack_techniques"].notnull()][
            ["capec_id", "attack_techniques"]
        ].rename(columns={"capec_id": "source", "attack_techniques": "target"})

        rel_dfs[CAPECPatternMapsToAttackTechnique.__relationshiptype__] = {
            "src_df": attack_df[["source"]].copy(),
            "tgt_df": attack_df[["target"]].copy(),
        }

        # CAPECPatternRelatesToCWE

        cwe_df = full_df.explode("cwes", ignore_index=True).copy()

        cwe_df = cwe_df.loc[cwe_df["cwes"].notnull()][["capec_id", "cwes"]].rename(
            columns={"capec_id": "source", "cwes": "target"}
        )

        rel_dfs[CAPECPatternRelatesToCWE.__relationshiptype__] = {
            "src_df": cwe_df[["source"]].copy(),
            "tgt_df": cwe_df[["target"]].copy(),
        }

        return node_dfs, rel_dfs
