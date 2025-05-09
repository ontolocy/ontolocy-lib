from io import BytesIO, TextIOWrapper
from zipfile import ZipFile

import pandas as pd
import requests
import xmltodict

from ontolocy import CWE

from .ontolocy_parser import OntolocyParser


class CWEParser(OntolocyParser):
    """Parser for MITRE's Common Weakness Enumerations

    https://cwe.mitre.org/

    Expects a zipped XML file. For example:

    https://cwe.mitre.org/data/xml/cwec_latest.xml.zip

    """

    node_types = [CWE]
    rel_types = []

    def _detect(self, input_data) -> bool:
        try:
            catalog = input_data.get("Weakness_Catalog", {}).get("@Name")

        except AttributeError:
            return False

        if catalog == "CWE":
            return True

        else:
            return False

    def _load_data(self, raw_data):
        """Expects raw zip file bytes"""

        bytes_data = BytesIO(raw_data)

        with ZipFile(bytes_data) as cwe_zip:
            filename = cwe_zip.namelist()[0]

            with TextIOWrapper(cwe_zip.open(filename, "r")) as f:
                data = f.read()

        return xmltodict.parse(data)

    def _load_file(self, file_path):
        with open(file_path, "rb") as f:  # type: ignore [arg-type]
            data = f.read()

        return data

    def _load_url(self, url):
        response = requests.get(url)

        return response.content

    def _parse(self, input_data, private_namespace=None) -> tuple:
        node_dfs = {}
        rel_dfs = {}

        weakness_catalogue = input_data.get("Weakness_Catalog", [])

        records = [
            {
                "cwe_id": x["@ID"],
                "description": x["Description"],
                "name": x["@Name"],
                "abstraction": x["@Abstraction"],
                "structure": x["@Structure"],
                "status": x["@Status"],
            }
            for x in weakness_catalogue["Weaknesses"]["Weakness"]
        ]

        full_df = pd.DataFrame.from_records(records)

        #
        # Nodes
        #

        cwe_df = full_df[
            ["cwe_id", "description", "name", "abstraction", "structure", "status"]
        ].copy()

        node_dfs[CWE.__primarylabel__] = cwe_df

        return node_dfs, rel_dfs
