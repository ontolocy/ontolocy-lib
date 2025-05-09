from datetime import datetime
from typing import Optional

from pydantic import Field, ValidationInfo, field_validator


class OntolocyMixin:
    ontolocy_merged: datetime = Field(
        default_factory=datetime.now,
    )

    # created property will only be set 'on create' - when the node is first created
    ontolocy_created: Optional[datetime] = Field(
        default=None, validate_default=True, json_schema_extra={"set_on_create": True}
    )

    # Use Pydantic's validator functionality to set created off the merged value
    @field_validator("ontolocy_created")
    def set_created_to_merged(
        cls, value: Optional[datetime], values: ValidationInfo
    ) -> datetime:
        """When the node is first created, we want the created value to be set equal to merged.
        Otherwise they will be a tiny amount of time different.
        """

        # set created = merged (which was set to datetime.now())
        if value is None:
            return values.data["ontolocy_merged"]

        # if the created value has been manually set, don't override it
        else:
            return value
