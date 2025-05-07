import warnings
from typing import Optional
from uuid import UUID, uuid5

import pandas as pd
from neontology import Neo4jConfig, init_neontology


def init_ontolocy(
    neo4j_uri: Optional[str] = None,
    neo4j_username: Optional[str] = None,
    neo4j_password: Optional[str] = None,
) -> None:
    """Initialise ontolocy.

    Wraps the init_neontology function.

    Args:
        neo4j_uri (Optional[str], optional): Neo4j URI to connect to. Defaults to None.
        neo4j_username (Optional[str], optional): Neo4j username. Defaults to None.
        neo4j_password (Optional[str], optional): Neo4j password. Defaults to None.
    """

    warnings.warn(
        "init_ontolocy function is being deprecated, use init_neontology directly from the Neontology library instead",
        DeprecationWarning,
    )

    neo4j_config = Neo4jConfig(
        uri=neo4j_uri, username=neo4j_username, password=neo4j_password
    )

    init_neontology(neo4j_config)


def generate_deterministic_uuid(values: list) -> UUID:
    # we use an arbitrary 'ontolocy' specific namespace
    namespace = UUID("8e43adb2-a389-4e4b-8012-3bc5702fb832")

    # create a single long string from all the values provided
    value_string = "".join([str(x) for x in values])

    generated_id = uuid5(namespace, value_string)

    return generated_id


def generate_str_id(values: list) -> str:
    # create a single long string from all the values provided
    value_string = (
        "-".join([str(x) for x in values if x is not None])
        .replace(".", "-")
        .replace(" ", "-")
    )

    cleaned_components = "".join(
        c for c in value_string if c.isalnum() or c in ["-", "_"]
    ).lower()

    return cleaned_components


def explode_map_dfs(df, to_map):
    input_df = df.copy()

    to_map_df = pd.concat(to_map)

    # keep a record of the original order
    input_df.insert(0, "ontolocy_merging_order", range(0, len(input_df)))

    merge_cols = list(set(to_map_df.columns) & set(input_df.columns))

    output_df = (
        input_df.merge(
            to_map_df,
            how="inner",
            on=merge_cols,
        )
        .sort_values("ontolocy_merging_order", ignore_index=True)
        .copy()
    ).drop(columns="ontolocy_merging_order")

    return output_df
