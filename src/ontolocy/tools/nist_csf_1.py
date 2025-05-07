import re
from io import BytesIO

import pandas as pd
import requests

from ontolocy import Control, ControlHasParentControl

from .ontolocy_parser import OntolocyParser


class NistCSF1Parser(OntolocyParser):
    """Parser for NIST CSF 1.1 data.

    https://www.nist.gov/document/2018-04-16frameworkv11core1xlsx
    """

    node_types = [Control]
    rel_types = [ControlHasParentControl]

    def _detect(self, input_data) -> bool:
        columns = [
            "Function",
            "Category",
            "Subcategory",
            "Informative References",
        ]

        try:
            input_columns = list(input_data.columns)

        except AttributeError:
            return False

        if input_columns == columns:
            return True

        return False

    def parse_data(self, input_data: pd.DataFrame, populate=True):
        """Parse NIST CSF v1.1 data.

        Args:
            input_data (DataFrame): Pandas DataFrame from reading CSF xlsx file.
            populate (bool, optional): whether to ingest the data. Defaults to True.
        """
        if self.detect(input_data) is False:
            raise ValueError(
                "Detection suggests input data is not valid for this parser"
            )

        self._process_data(input_data)

        if populate is True:
            self.populate()

    def _load_data(self, raw_data):
        return pd.read_excel(BytesIO(raw_data))

    def _load_file(self, file_path):
        with open(file_path, "rb") as f:  # type: ignore [arg-type]
            data = f.read()

        return data

    def _load_url(self, url):
        response = requests.get(url)

        return response.content

    def _parse(self, input_data: pd.DataFrame, private_namespace=None) -> tuple:
        FRAMEWORK = "NIST CSF"
        FRAMEWORK_VERSION = "1.1"
        FRAMEWORK_URL = "https://doi.org/10.6028/NIST.CSWP.04162018"

        node_dfs = {}
        rel_dfs = {}

        df = input_data.ffill()

        #
        # Nodes
        #

        # Functions

        functions_df = pd.DataFrame()
        functions_df["name"] = pd.Series(df["Function"].unique()).map(
            lambda x: x.split()[0].title()
        )
        functions_df["control_id"] = pd.Series(df["Function"].unique()).map(
            lambda x: x.split()[1][1:3]
        )

        # Function descriptions from "https://doi.org/10.6028/NIST.CSWP.04162018"
        functions_df["description"] = [
            (
                "Develop an organizational understanding to manage cybersecurity"
                " risk to systems, people, assets, data, and capabilities."
            ),
            (
                "Develop and implement appropriate safeguards to ensure delivery"
                " of critical services."
            ),
            (
                "Develop and implement appropriate activities to identify the"
                " occurrence of a cybersecurity event."
            ),
            (
                "Develop and implement appropriate activities to take action"
                " regarding a detected cybersecurity incident."
            ),
            (
                "Develop and implement appropriate activities to maintain plans for"
                " resilience and to restore any capabilities or services that were"
                " impaired due to a cybersecurity incident."
            ),
        ]

        functions_df["framework"] = FRAMEWORK
        functions_df["framework_level"] = "Function"
        functions_df["framework_version"] = FRAMEWORK_VERSION
        functions_df["url_reference"] = FRAMEWORK_URL

        def row_to_id(row):
            control = Control(**row.to_dict())
            return control.unique_id

        functions_df["unique_id"] = functions_df.apply(row_to_id, axis=1)

        # Categories

        categories_df = pd.DataFrame()
        categories_df["name"] = pd.Series(df["Category"].unique()).map(
            lambda x: x.split("(")[0].strip()
        )
        categories_df["description"] = pd.Series(df["Category"].unique()).map(
            lambda x: x.split(":")[1].strip()
        )
        categories_df["control_id"] = pd.Series(df["Category"].unique()).map(
            lambda x: re.search(r"[A-Z]{2}\.[A-Z]{2}", x).group()
        )
        categories_df["framework"] = FRAMEWORK
        categories_df["framework_level"] = "Category"
        categories_df["framework_version"] = FRAMEWORK_VERSION
        categories_df["url_reference"] = FRAMEWORK_URL

        categories_df["unique_id"] = categories_df.apply(row_to_id, axis=1)

        # Subcategories

        subcategories_df = pd.DataFrame()
        subcategories_df["name"] = pd.Series(df["Subcategory"].unique()).map(
            lambda x: x.split(":")[0].strip()
        )

        # for subcategories, the control_id is the name
        subcategories_df["control_id"] = subcategories_df["name"]

        subcategories_df["description"] = pd.Series(df["Subcategory"].unique()).map(
            lambda x: x.split(":")[1].strip()
        )
        subcategories_df["framework"] = FRAMEWORK
        subcategories_df["framework_level"] = "Subcategory"
        subcategories_df["framework_version"] = FRAMEWORK_VERSION
        subcategories_df["url_reference"] = FRAMEWORK_URL

        subcategories_df["unique_id"] = subcategories_df.apply(row_to_id, axis=1)

        all_controls_df = pd.concat([functions_df, categories_df, subcategories_df])

        node_dfs[Control.__primarylabel__] = all_controls_df.copy()

        #
        # Relationships
        #

        # Category to Function

        cat_to_func_df = pd.DataFrame()
        cat_to_func_df["source"] = categories_df["unique_id"]
        cat_to_func_df["target"] = categories_df["unique_id"].map(
            lambda x: x[:-3].replace("category", "function")
        )

        # Subcategory to Category

        subcat_to_cat_df = pd.DataFrame()
        subcat_to_cat_df["source"] = subcategories_df["unique_id"]
        subcat_to_cat_df["target"] = subcategories_df["unique_id"].map(
            lambda x: x[:30].replace("subcategory", "category")
        )

        parent_rels_df = pd.concat([cat_to_func_df, subcat_to_cat_df])
        parent_rels_df["url_reference"] = FRAMEWORK_URL

        rel_dfs[ControlHasParentControl.__relationshiptype__] = {
            "src_df": parent_rels_df[["source"]].copy(),
            "tgt_df": parent_rels_df[["target"]].copy(),
            "props_df": parent_rels_df[["url_reference"]].copy(),
        }

        # Related SP 800-53 Controls

        return node_dfs, rel_dfs
