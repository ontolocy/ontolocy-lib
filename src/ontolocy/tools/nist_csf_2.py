import re
import warnings
from io import BytesIO

import pandas as pd
import requests

from ontolocy import Control, ControlHasParentControl

from .ontolocy_parser import OntolocyParser


class NistCSF2Parser(OntolocyParser):
    """Parser for NIST CSF 2.0 data.

    https://csrc.nist.gov/extensions/nudp/services/json/csf/download?olirids=all

    """

    node_types = [Control]
    rel_types = [ControlHasParentControl]

    def _detect(self, input_data) -> bool:
        columns = [
            "Function",
            "Category",
            "Subcategory",
            "Implementation Examples",
            "Informative References",
        ]

        try:
            input_columns = input_data.columns.to_list()

        except AttributeError:
            # If the input is not a DataFrame, we can't detect it
            # When loading from a file, or URL, _load_data should convert it to a DataFrame
            return False

        if input_columns == columns:
            return True

        return False

    def _load_data(self, raw_data):
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                category=UserWarning,
                module=re.escape("openpyxl.styles.stylesheet"),
            )
            df = pd.read_excel(BytesIO(raw_data), sheet_name="CSF 2.0", skiprows=1)

        return df

    def _load_file(self, file_path):
        with open(file_path, "rb") as f:  # type: ignore [arg-type]
            data = f.read()

        return data

    def _load_url(self, url):
        response = requests.get(url)

        return response.content

    def _parse(self, input_data: pd.DataFrame, private_namespace=None) -> tuple:
        FRAMEWORK = "NIST CSF"
        FRAMEWORK_VERSION = "2.0"
        FRAMEWORK_URL = "https://doi.org/10.6028/NIST.CSWP.29"

        node_dfs = {}
        rel_dfs = {}

        df = input_data.copy()

        #
        # Nodes
        #

        def row_to_id(row):
            control = Control(**row.to_dict())
            return control.unique_id

        # Functions

        functions_df = df.loc[~df["Function"].isna()][
            ["Function", "Informative References"]
        ]
        functions_df = functions_df.loc[
            functions_df["Function"].str.contains(r"[A-Z]*\([A-Z]{2}\): ", na=False)
        ].copy()
        functions_df["name"] = functions_df["Function"].apply(
            lambda x: x.split(" ")[0].title()
        )
        functions_df["control_id"] = functions_df["Function"].apply(
            lambda x: x.split(" ")[1][1:3]
        )

        functions_df["description"] = functions_df["Function"].apply(
            lambda x: x.split(":")[1]
        )

        functions_df["framework"] = FRAMEWORK
        functions_df["framework_level"] = "Function"
        functions_df["framework_version"] = FRAMEWORK_VERSION
        functions_df["url_reference"] = FRAMEWORK_URL

        function_control_df = functions_df.drop(
            columns=["Function", "Informative References"]
        )

        function_control_df["unique_id"] = function_control_df.apply(row_to_id, axis=1)

        # Categories

        categories_df = df.loc[~df["Category"].isna()][
            ["Category", "Informative References"]
        ]
        categories_df = categories_df.loc[
            ~categories_df["Category"].str.contains("Withdrawn")
        ].copy()
        categories_df["name"] = categories_df["Category"].map(
            lambda x: x.split("(")[0].title()
        )
        categories_df["description"] = categories_df["Category"].map(
            lambda x: x.split(":")[1].strip()
        )
        categories_df["control_id"] = categories_df["Category"].map(
            lambda x: re.search(r"[A-Z]{2}\.[A-Z]{2}", x).group()
        )

        categories_df["framework"] = FRAMEWORK
        categories_df["framework_level"] = "Category"
        categories_df["framework_version"] = FRAMEWORK_VERSION
        categories_df["url_reference"] = FRAMEWORK_URL

        category_control_df = categories_df.drop(
            columns=["Category", "Informative References"]
        )

        category_control_df["unique_id"] = category_control_df.apply(row_to_id, axis=1)

        # Subcategories

        subcategories_df = df.loc[~df["Subcategory"].isna()][
            ["Subcategory", "Implementation Examples", "Informative References"]
        ]

        subcategories_df = subcategories_df.loc[
            ~subcategories_df["Subcategory"].str.contains("Withdrawn")
        ].copy()

        subcategories_df["name"] = subcategories_df["Subcategory"].map(
            lambda x: x.split(":")[0].strip()
        )

        # for subcategories, the control_id is the name
        subcategories_df["control_id"] = subcategories_df["name"]

        subcategories_df["description"] = subcategories_df["Subcategory"].map(
            lambda x: x.split(":")[1].strip()
        )
        subcategories_df["framework"] = FRAMEWORK
        subcategories_df["framework_level"] = "Subcategory"
        subcategories_df["framework_version"] = FRAMEWORK_VERSION
        subcategories_df["url_reference"] = FRAMEWORK_URL

        subcategory_control_df = subcategories_df.drop(
            columns=["Subcategory", "Informative References", "Implementation Examples"]
        )

        subcategory_control_df["unique_id"] = subcategory_control_df.apply(
            row_to_id, axis=1
        )

        all_controls_df = pd.concat(
            [function_control_df, category_control_df, subcategory_control_df]
        )

        node_dfs[Control.__primarylabel__] = all_controls_df.copy()

        #
        # Relationships
        #

        # Category to Function

        cat_to_func_df = pd.DataFrame()
        cat_to_func_df["source"] = category_control_df["unique_id"]
        cat_to_func_df["target"] = category_control_df["unique_id"].map(
            lambda x: x[:-3].replace("category", "function")
        )

        # Subcategory to Category

        subcat_to_cat_df = pd.DataFrame()
        subcat_to_cat_df["source"] = subcategory_control_df["unique_id"]
        subcat_to_cat_df["target"] = subcategory_control_df["unique_id"].map(
            lambda x: x[:30].replace("subcategory", "category")
        )

        parent_rels_df = pd.concat([cat_to_func_df, subcat_to_cat_df])
        parent_rels_df["url_reference"] = FRAMEWORK_URL

        rel_dfs[ControlHasParentControl.__relationshiptype__] = {
            "src_df": parent_rels_df[["source"]].copy(),
            "tgt_df": parent_rels_df[["target"]].copy(),
            "props_df": parent_rels_df[["url_reference"]].copy(),
        }

        # Implementation Examples

        # Related CSF 1.1 Controls

        # Related SP800-53 r5 Controls

        return node_dfs, rel_dfs
