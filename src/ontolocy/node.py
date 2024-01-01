from typing import ClassVar, Optional
from warnings import warn

import pandas as pd
from neontology import BaseNode

from .dataorigin import DataOrigin, OriginGenerated


class OntolocyNode(BaseNode, validate_default=True):
    __primarylabel__: ClassVar[Optional[str]] = None

    @classmethod
    def ingest_df(
        cls,
        df: pd.DataFrame,
        data_origin: Optional[DataOrigin] = None,
        deduplicate=True,
    ) -> list:
        nodes = cls.merge_df(df, deduplicate=deduplicate)

        if data_origin is not None:
            data_origin.merge()

            rels = [OriginGenerated(source=data_origin, target=x) for x in nodes]

            OriginGenerated.merge_relationships(rels, target_type=cls)

        return nodes

    def ingest(
        self,
        data_origin: Optional[DataOrigin] = None,
    ) -> None:
        # first merge in this node
        self.merge()

        # if a data_origin is specified, merge that and then create the OriginGenerated relationship
        if data_origin is not None:
            data_origin.merge()

            rel = OriginGenerated(source=data_origin, target=self)

            rel.merge()

    def get_identifier(self) -> str:
        warn("'get_identifier' method is deprecated", DeprecationWarning)
        return str(self.get_primary_property_value())

    def __str__(self) -> str:
        return str(self.get_primary_property_value())
