from abc import ABC
from typing import Optional

import pandas as pd
from neontology import BaseRelationship

from .dataorigin import DataOrigin


class OntolocyRelationship(BaseRelationship, ABC):

    data_origin_name: Optional[str]
    data_origin_reference: Optional[str]
    data_origin_license: Optional[str]
    data_origin_sharing: Optional[str]

    @classmethod
    def ingest_df(
        cls,
        df: pd.DataFrame,
        data_origin: Optional[DataOrigin] = None,
        source_prop: Optional[str] = None,
        target_prop: Optional[str] = None,
    ):

        input_df = df.copy()

        if data_origin is not None:
            input_df["data_origin_name"] = data_origin.name
            input_df["data_origin_reference"] = data_origin.reference
            input_df["data_origin_license"] = data_origin.license
            input_df["data_origin_sharing"] = data_origin.sharing

        return cls.merge_df(input_df, source_prop=source_prop, target_prop=target_prop)
