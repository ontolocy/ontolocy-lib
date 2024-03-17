from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, List, Optional

import pandas as pd

from ..dataorigin import DataOrigin
from ..node import OntolocyNode
from ..relationship import OntolocyRelationship


class IngesterBase(ABC):
    node_types: List[OntolocyNode] = []
    rel_types: List[OntolocyRelationship] = []
    relationship_kwargs: dict = {}

    def __init__(
        self,
        data_origin: Optional[DataOrigin] = None,
        private_namespace: Optional[str] = None,
        auto_namespace: Optional[bool] = True,
        assign_data_origin: Optional[bool] = False,
    ) -> None:
        super().__init__()

        self.data_inputs: list = []

        self.node_oriented_dfs: Dict[str, pd.DataFrame] = {}
        self.rel_input_dfs: Dict[str, pd.DataFrame] = defaultdict(dict)
        self.rel_oriented_dfs: Dict[str, pd.DataFrame] = {}

        self.auto_namespace = auto_namespace

        if data_origin is None:
            data_origin_name = self.__class__.__name__

            data_origin = DataOrigin(
                name=data_origin_name,
            )

        if private_namespace:
            self.private_namespace = private_namespace

        else:
            self.private_namespace = None

        if assign_data_origin is True:
            self.data_origin = data_origin

            self.data_origin_dict = {
                "data_origin_name": self.data_origin.name,
                "data_origin_reference": self.data_origin.reference,
                "data_origin_license": self.data_origin.license,
                "data_origin_sharing": self.data_origin.sharing,
            }

        else:
            self.data_origin = None

    def _process_data(self, input_data, private_namespace=None):
        """
        Takes input data in the form of a tuple of dicts:
            Nodes: indexed by node label - with corresponding df for all nodes to merge
            Rels: indexed by rel type - with src, tgt and (optional) rel_props dfs for each

        Drop any duplicates.

        If the ingestor has already been run on different data, append the new data
        """

        self.data_inputs.append(input_data)

        node_oriented_dfs, rel_input_dfs = self._parse(input_data, private_namespace)

        # update node entries
        for label, df in node_oriented_dfs.items():
            # drop any duplicates

            df.drop_duplicates(ignore_index=True, inplace=True)
            self.node_oriented_dfs[label] = pd.concat(
                [self.node_oriented_dfs.get(label, pd.DataFrame()), df]
            )

        # update relationship entries
        for rel_type, entry in rel_input_dfs.items():
            for key, df in entry.items():
                self.rel_input_dfs[rel_type][key] = pd.concat(
                    [
                        self.rel_input_dfs.get(rel_type, {}).get(key, pd.DataFrame()),
                        df,
                    ]
                )

    def _merge_nodes(self) -> None:
        for node_type in self.node_types:
            df = self.node_oriented_dfs[node_type.__primarylabel__]

            if "ontolocy_parser_node_pp" in df.columns:
                nodes = node_type.ingest_df(
                    df.drop(columns=["ontolocy_parser_node_pp"]),
                    self.data_origin,
                )

            else:
                nodes = node_type.ingest_df(
                    df,
                    self.data_origin,
                )

            df["ontolocy_parser_node_pp"] = [
                x.get_primary_property_value() for x in nodes
            ]

    def _generate_relationships(self) -> None:
        for rel_type in self.rel_types:
            dfs = self.rel_input_dfs[rel_type.__relationshiptype__]

            if "props_df" in dfs:
                new_df = dfs.get("props_df").reset_index(drop=True).copy()

            else:
                new_df = pd.DataFrame()

            source_label = rel_type.model_fields["source"].annotation.__primarylabel__

            if "src_df" in dfs and "tgt_df" in dfs:
                # where we only need to specify a single field to match on
                # the src_df should just have one column: 'source'
                # this applies to situations where we aren't creating the nodes in this parser
                # or where the property to match on is deterministic / easy to work out
                if list(dfs["src_df"].columns) == ["source"]:
                    new_df["source"] = (
                        dfs["src_df"]["source"].reset_index(drop=True).copy()
                    )

                # newly created nodes may need to have their ids looked up
                # for example, where the primary property has to be calculated
                elif source_label in self.node_oriented_dfs:
                    src_cols = list(dfs["src_df"].columns) + ["ontolocy_parser_node_pp"]

                    src_df = self.node_oriented_dfs[source_label][src_cols].copy()

                    merged_src_df = (
                        dfs["src_df"]
                        .merge(src_df, how="left")["ontolocy_parser_node_pp"]
                        .copy()
                    )

                    new_df["source"] = merged_src_df

                else:
                    raise (
                        ValueError(
                            "Inappropriately formed source relationship data frames"
                        )
                    )

                target_label = rel_type.model_fields[
                    "target"
                ].annotation.__primarylabel__

                # if we just have a 'target' column, use this to match on
                if list(dfs["tgt_df"].columns) == ["target"]:
                    new_df["target"] = (
                        dfs["tgt_df"]["target"].reset_index(drop=True).copy()
                    )

                # newly created nodes need to have their ids looked up
                elif target_label in self.node_oriented_dfs:
                    tgt_cols = list(dfs["tgt_df"].columns) + ["ontolocy_parser_node_pp"]

                    tgt_df = self.node_oriented_dfs[target_label][tgt_cols].copy()

                    merged_tgt_df = (
                        dfs["tgt_df"]
                        .merge(tgt_df, how="left")["ontolocy_parser_node_pp"]
                        .copy()
                    )

                    new_df["target"] = merged_tgt_df

                else:
                    raise (
                        ValueError(
                            "Inappropriately formed target relationship data frames"
                        )
                    )

            self.rel_oriented_dfs[rel_type.__relationshiptype__] = new_df

    def _merge_relationships(self) -> None:
        for rel_type_class in self.rel_types:

            rel_type = rel_type_class.__relationshiptype__

            df = self.rel_oriented_dfs[rel_type]

            kwargs = self.relationship_kwargs.get(rel_type, {})

            rel_type_class.ingest_df(df, self.data_origin, **kwargs)

    def populate(
        self,
    ) -> None:

        self._merge_nodes()
        self._generate_relationships()
        self._merge_relationships()

    @abstractmethod
    def _parse(self, input_data, private_namespace=None) -> tuple:
        """Returns a tuple where the first entry is a dictionary of node dataframes indexed by label
        The second entry is a dictionary of relationship dataframes indexed by relationship type
            Each relationship entry includes the following:
                * "src_df"
                * "tgt_df"
                * "props_df"
            If the relationship source/target is a node that hasn't just been created,
            then we just expect a single column (source/target).
            Newly created nodes expect sufficient columns to uniquely match the entry in the node df

        """
        raise NotImplementedError
