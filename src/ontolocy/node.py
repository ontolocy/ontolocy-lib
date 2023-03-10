from typing import ClassVar, Optional

import pandas as pd
from neontology import BaseNode

from .dataorigin import DataOrigin, OriginGenerated


class OntolocyNode(BaseNode):
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

        # if a data_origin is specified, merge that and then creat the OriginGenerated relationship
        if data_origin is not None:
            data_origin.merge()

            rel = OriginGenerated(source=data_origin, target=self)

            rel.merge()
