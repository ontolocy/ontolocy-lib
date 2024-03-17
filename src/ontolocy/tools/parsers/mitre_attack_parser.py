import json

import pandas as pd

from ontolocy import (
    MitreAttackCampaign,
    MitreAttackDataComponent,
    MitreAttackDataComponentDetectsTechnique,
    MitreAttackDataSource,
    MitreAttackDataSourceHasComponent,
    MitreAttackGroup,
    MitreAttackGroupUsesSoftware,
    MitreAttackGroupUsesTechnique,
    MitreAttackMitigation,
    MitreAttackMitigationDefendsAgainstTechnique,
    MitreAttackSoftware,
    MitreAttackTactic,
    MitreAttackTechnique,
    MitreCampaignAttributedTo,
    MitreCampaignUsesSoftware,
    MitreCampaignUsesTechnique,
    MitreSoftwareUsesTechnique,
    MitreSubtechniqueOf,
    MitreTacticIncludesTechnique,
)

from .ontolocy_parser import OntolocyParser


class MitreAttackParser(OntolocyParser):
    node_types = [
        MitreAttackCampaign,
        MitreAttackSoftware,
        MitreAttackTactic,
        MitreAttackTechnique,
        MitreAttackDataSource,
        MitreAttackDataComponent,
        MitreAttackMitigation,
        MitreAttackGroup,
    ]
    rel_types = [
        MitreTacticIncludesTechnique,
        MitreAttackGroupUsesTechnique,
        MitreAttackGroupUsesSoftware,
        MitreSubtechniqueOf,
        MitreCampaignUsesSoftware,
        MitreCampaignAttributedTo,
        MitreCampaignUsesTechnique,
        MitreSoftwareUsesTechnique,
        MitreAttackMitigationDefendsAgainstTechnique,
        MitreAttackDataComponentDetectsTechnique,
        MitreAttackDataSourceHasComponent,
    ]

    def _detect(self, input_data) -> bool:
        try:
            stix_json = json.loads(input_data)

        except json.decoder.JSONDecodeError:
            print("json decode error")
            return False

        if "x_mitre_attack_spec_version" in stix_json["objects"][0]:
            return True

        else:
            return False

    def _stix_objects_to_df(self, stix_data, stix_types):
        """Pull out stix objects of a certain type"""

        all_allowed_columns = set(
            [
                "stix_id",
                "stix_type",
                "stix_spec_version",
                "stix_created",
                "stix_modified",
                "stix_revoked",
                "attack_version",
                "attack_spec_version",
                "attack_id",
                "ref_url",
                "name",
                "description",
                "attack_subtechnique",
                "attack_shortname",
                "stix_first_seen",
                "stix_last_seen",
                "attack_first_seen_citation",
                "attack_last_seen_citation",
                "kill_chain_phase_list",
                "aliases",
                "x_mitre_data_source_ref",
                "attack_deprecated",
            ]
        )

        attack_objs = [
            x
            for x in stix_data["objects"]
            if x["type"] in stix_types
            # and not x.get("x_mitre_deprecated")
            # and not x.get("revoked")
        ]

        # pull out associated MITRE ATT&CK tactics the MITRE ATT&CK reference (web address)
        for attack_obj in attack_objs:

            if attack_obj.get("kill_chain_phases"):
                attack_obj["kill_chain_phase_list"] = []

                for phase in attack_obj.get("kill_chain_phases", []):
                    if phase["kill_chain_name"] == "mitre-attack":
                        attack_obj["kill_chain_phase_list"].append(phase["phase_name"])

            for ref in attack_obj.get("external_references", []):
                if ref["source_name"] == "mitre-attack":
                    attack_obj["attack_id"] = ref["external_id"]
                    attack_obj["ref_url"] = ref["url"]
                    break

        df = pd.DataFrame.from_records(attack_objs).rename(
            columns={
                "id": "stix_id",
                "type": "stix_type",
                "created": "stix_created",
                "modified": "stix_modified",
                "spec_version": "stix_spec_version",
                "revoked": "stix_revoked",
                "x_mitre_version": "attack_version",
                "x_mitre_is_subtechnique": "attack_subtechnique",
                "x_mitre_attack_spec_version": "attack_spec_version",
                "x_mitre_shortname": "attack_shortname",
                "first_seen": "stix_first_seen",
                "last_seen": "stix_last_seen",
                "x_mitre_first_seen_citation": "attack_first_seen_citation",
                "x_mitre_last_seen_citation": "attack_last_seen_citation",
                "x_mitre_deprecated": "attack_deprecated",
            }
        )

        all_columns = set(df.columns)

        drop_columns = all_columns.difference(all_allowed_columns)

        df_subset = df.drop(columns=list(drop_columns))

        return df_subset

    def _stix_rels_to_df(self, stix_data):
        rel_objs = [x for x in stix_data["objects"] if x["type"] == "relationship"]

        rel_df = pd.DataFrame.from_records(rel_objs)

        return rel_df

    def _parse(self, input_data, private_namespace=None) -> tuple:
        stix_json = json.loads(input_data)

        #
        # Nodes
        #

        node_dfs = {}

        tactics_df = self._stix_objects_to_df(stix_json, ["x-mitre-tactic"])

        tactics_dict = (
            tactics_df[["attack_shortname", "stix_id"]]
            .set_index("attack_shortname")["stix_id"]
            .to_dict()
        )

        node_dfs[MitreAttackTactic.__primarylabel__] = tactics_df.copy()

        techniques_df = self._stix_objects_to_df(stix_json, ["attack-pattern"])

        node_dfs[MitreAttackTechnique.__primarylabel__] = techniques_df.drop(
            columns=["kill_chain_phase_list"]
        ).copy()

        groups_df = self._stix_objects_to_df(stix_json, ["intrusion-set"])

        node_dfs[MitreAttackGroup.__primarylabel__] = groups_df.drop(
            columns=["aliases"]
        ).copy()

        campaigns_df = self._stix_objects_to_df(stix_json, ["campaign"])

        node_dfs[MitreAttackCampaign.__primarylabel__] = campaigns_df.drop(
            columns=["aliases"]
        ).copy()

        software_df = self._stix_objects_to_df(stix_json, ["tool", "malware"])

        node_dfs[MitreAttackSoftware.__primarylabel__] = software_df.copy()

        mitigations_df = self._stix_objects_to_df(stix_json, ["course-of-action"])

        node_dfs[MitreAttackMitigation.__primarylabel__] = mitigations_df.copy()

        datasources_df = self._stix_objects_to_df(stix_json, ["x-mitre-data-source"])

        node_dfs[MitreAttackDataSource.__primarylabel__] = datasources_df.copy()

        datacomponents_df = self._stix_objects_to_df(
            stix_json, ["x-mitre-data-component"]
        )

        if datacomponents_df.empty is False:

            node_dfs[
                MitreAttackDataComponent.__primarylabel__
            ] = datacomponents_df.drop(columns=["x_mitre_data_source_ref"]).copy()

        else:
            node_dfs[MitreAttackDataComponent.__primarylabel__] = pd.DataFrame()

        #
        # Relationships
        #

        rel_dfs = {}

        all_relationships_df = self._stix_rels_to_df(stix_json).rename(
            columns={"source_ref": "source", "target_ref": "target"}
        )

        # Techniques to Tactics

        tactic_technique_df = pd.DataFrame()

        for technique_row in techniques_df.iterrows():
            target = technique_row[1].stix_id

            sources = [tactics_dict[x] for x in technique_row[1].kill_chain_phase_list]

            entry_df = pd.DataFrame()
            entry_df["source"] = sources
            entry_df["target"] = target

            tactic_technique_df = pd.concat([tactic_technique_df, entry_df])

        rel_dfs[MitreTacticIncludesTechnique.__relationshiptype__] = {
            "src_df": tactic_technique_df[["source"]].copy(),
            "tgt_df": tactic_technique_df[["target"]].copy(),
        }

        # Techniques to Subtechniques

        techniques_to_subtechniques_df = all_relationships_df.loc[
            all_relationships_df.source.str.startswith("attack-pattern")
            & all_relationships_df.target.str.startswith("attack-pattern")
            & all_relationships_df.relationship_type.str.match("subtechnique-of")
        ]

        rel_dfs[MitreSubtechniqueOf.__relationshiptype__] = {
            "src_df": techniques_to_subtechniques_df[["source"]].copy(),
            "tgt_df": techniques_to_subtechniques_df[["target"]].copy(),
        }

        # Group to Technique

        group_to_technique_df = all_relationships_df.loc[
            all_relationships_df.source.str.startswith("intrusion-set")
            & all_relationships_df.target.str.startswith("attack-pattern")
        ]

        rel_dfs[MitreAttackGroupUsesTechnique.__relationshiptype__] = {
            "src_df": group_to_technique_df[["source"]].copy(),
            "tgt_df": group_to_technique_df[["target"]].copy(),
        }

        # Group to Software

        group_to_software_df = all_relationships_df.loc[
            all_relationships_df.source.str.startswith("intrusion-set")
            & (
                all_relationships_df.target.str.startswith("tool")
                | all_relationships_df.target.str.startswith("malware")
            )
        ]

        rel_dfs[MitreAttackGroupUsesSoftware.__relationshiptype__] = {
            "src_df": group_to_software_df[["source"]].copy(),
            "tgt_df": group_to_software_df[["target"]].copy(),
        }

        # Campaigns to Software

        campaign_to_software_df = all_relationships_df.loc[
            all_relationships_df.source.str.startswith("campaign")
            & (
                all_relationships_df.target.str.startswith("tool")
                | all_relationships_df.target.str.startswith("malware")
            )
        ]

        rel_dfs[MitreCampaignUsesSoftware.__relationshiptype__] = {
            "src_df": campaign_to_software_df[["source"]].copy(),
            "tgt_df": campaign_to_software_df[["target"]].copy(),
        }

        # Campaigns to Techniques

        campaign_to_technique_df = all_relationships_df.loc[
            all_relationships_df.source.str.startswith("campaign")
            & all_relationships_df.target.str.startswith("attack-pattern")
        ]

        rel_dfs[MitreCampaignUsesTechnique.__relationshiptype__] = {
            "src_df": campaign_to_technique_df[["source"]].copy(),
            "tgt_df": campaign_to_technique_df[["target"]].copy(),
        }

        # Campaigns to Intrusion Sets

        campaign_to_intrusion_set_df = all_relationships_df.loc[
            all_relationships_df.source.str.startswith("campaign")
            & all_relationships_df.target.str.startswith("intrusion-set")
            & all_relationships_df.relationship_type.str.match("attributed-to")
        ]

        rel_dfs[MitreCampaignAttributedTo.__relationshiptype__] = {
            "src_df": campaign_to_intrusion_set_df[["source"]].copy(),
            "tgt_df": campaign_to_intrusion_set_df[["target"]].copy(),
        }

        # Software to Techniques

        software_to_technique_df = all_relationships_df.loc[
            (
                all_relationships_df.source.str.startswith("tool")
                | all_relationships_df.source.str.startswith("malware")
            )
            & all_relationships_df.target.str.startswith("attack-pattern")
        ]

        rel_dfs[MitreSoftwareUsesTechnique.__relationshiptype__] = {
            "src_df": software_to_technique_df[["source"]].copy(),
            "tgt_df": software_to_technique_df[["target"]].copy(),
        }

        # Mitigation to Techniques

        mitigation_to_technique_df = all_relationships_df.loc[
            all_relationships_df.source.str.startswith("course-of-action")
            & all_relationships_df.target.str.startswith("attack-pattern")
            & all_relationships_df.relationship_type.str.match("mitigates")
        ]

        rel_dfs[MitreAttackMitigationDefendsAgainstTechnique.__relationshiptype__] = {
            "src_df": mitigation_to_technique_df[["source"]].copy(),
            "tgt_df": mitigation_to_technique_df[["target"]].copy(),
        }

        # Data Component to Techniques

        mitigation_to_technique_df = all_relationships_df.loc[
            all_relationships_df.source.str.startswith("x-mitre-data-component")
            & all_relationships_df.target.str.startswith("attack-pattern")
            & all_relationships_df.relationship_type.str.match("detects")
        ]

        rel_dfs[MitreAttackDataComponentDetectsTechnique.__relationshiptype__] = {
            "src_df": mitigation_to_technique_df[["source"]].copy(),
            "tgt_df": mitigation_to_technique_df[["target"]].copy(),
        }

        # Data Source to Data Component

        if datacomponents_df.empty is False:

            data_source_to_component_df = pd.DataFrame()

            data_source_to_component_df["source"] = datacomponents_df[
                "x_mitre_data_source_ref"
            ]
            data_source_to_component_df["target"] = datacomponents_df["stix_id"]

            rel_dfs[MitreAttackDataSourceHasComponent.__relationshiptype__] = {
                "src_df": data_source_to_component_df[["source"]].copy(),
                "tgt_df": data_source_to_component_df[["target"]].copy(),
            }

        return node_dfs, rel_dfs
