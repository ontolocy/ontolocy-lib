from datetime import datetime
from typing import ClassVar, Optional
from warnings import warn

import pandas as pd
from neontology import BaseNode
from pydantic import Field, ValidationInfo, field_validator

from .dataorigin import DataOrigin, OriginGenerated


class OntolocyNode(BaseNode, validate_default=True):
    __primarylabel__: ClassVar[Optional[str]] = None

    merged: datetime = Field(
        default_factory=datetime.now,
    )

    # created property will only be set 'on create' - when the node is first created
    created: Optional[datetime] = Field(
        default=None, validate_default=True, json_schema_extra={"set_on_create": True}
    )

    # Use Pydantic's validator functionality to set created off the merged value
    @field_validator("created")
    def set_created_to_merged(
        cls, value: Optional[datetime], values: ValidationInfo
    ) -> datetime:
        """When the node is first created, we want the created value to be set equal to merged.
        Otherwise they will be a tiny amount of time different.
        """

        # set created = merged (which was set to datetime.now())
        if value is None:
            return values.data["merged"]

        # if the created value has been manually set, don't override it
        else:
            return value

    @classmethod
    def ingest_df(
        cls,
        df: pd.DataFrame,
        data_origin: Optional[DataOrigin] = None,
        deduplicate=True,
    ) -> pd.Series:
        nodes = cls.merge_df(df, deduplicate=deduplicate)

        if data_origin is not None:
            data_origin.merge()

            rels = [OriginGenerated(source=data_origin, target=x) for x in nodes]

            OriginGenerated.merge_relationships(rels)

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
        return str(self.get_pp())

    def __str__(self) -> str:
        return str(self.get_pp())
