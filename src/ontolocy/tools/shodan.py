import json
import os

import pandas as pd
import shodan

from ontolocy import (
    Banner,
    IPAddressHasOpenPort,
    IPAddressNode,
    JarmHash,
    ListeningSocket,
    ListeningSocketHasBanner,
    ListeningSocketHasJarmHash,
    ListeningSocketHasX509Certificate,
    ListeningSocketUsesPort,
    Port,
    X509Certificate,
)

from .ontolocy_enricher import OntolocyClient, OntolocyEnricher, SeedTypeEnum
from .ontolocy_parser import OntolocyParser


class ShodanParser(OntolocyParser):
    node_types = [
        IPAddressNode,
        Port,
        ListeningSocket,
        X509Certificate,
        JarmHash,
        Banner,
    ]

    rel_types = [
        IPAddressHasOpenPort,
        ListeningSocketUsesPort,
        ListeningSocketHasBanner,
        ListeningSocketHasX509Certificate,
        ListeningSocketHasJarmHash,
    ]

    def _detect(self, input_data) -> bool:
        try:
            data = input_data.get("matches")

        except AttributeError:
            return False

        if len(data) == 0:
            return False

        if (
            "data" in data[0]
            and "domains" in data[0]
            and "hostnames" in data[0]
            and "ip" in data[0]
        ):
            return True

        else:
            return False

    def _load_data(self, raw_data):
        return json.loads(raw_data)

    def _generate_df(self, raw_data):
        try:
            data = json.loads(raw_data).get("matches")
        except TypeError:
            data = raw_data.get("matches")

        all_results = [
            {
                "ip_address": x["ip_str"],
                "asn": x.get("asn"),
                "protocol": x.get("transport"),
                "port_number": x.get("port"),
                "CPEs": x.get("CPE"),
                "hostnames": x.get("hostnames"),
                "domains": x.get("domains"),
                "http_title": x.get("http", {}).get("title"),
                "security_txt": x.get("http", {}).get("securitytxt"),
                "banner": x.get("data"),
                "latitude": x.get("location", {}).get("latitude"),
                "longitude": x.get("location", {}).get("longitude"),
                "city": x.get("location", {}).get("city"),
                "country_name": x.get("location", {}).get("country_name"),
                "country_code": x.get("location", {}).get("country_code"),
                "org": x.get("org"),
                "jarm": x.get("ssl", {}).get("jarm"),
                "sha1": x.get("ssl", {})  # TLS certificate sha1
                .get("cert", {})
                .get("fingerprint", {})
                .get("sha1"),
                "sha256": x.get("ssl", {})  # TLS certificate sha256
                .get("cert", {})
                .get("fingerprint", {})
                .get("sha256"),
                "serial_number": str(
                    x.get("ssl", {}).get("cert", {}).get("serial")
                ),  # TLS certificate serial number
                "subject_country": x.get("ssl", {})  # TLS certificate subject country
                .get("cert", {})
                .get("subject", {})
                .get("C"),
                "subject_cn": x.get("ssl", {})  # TLS certificate subject common name
                .get("cert", {})
                .get("subject", {})
                .get("CN"),
                "subject_ou": x.get(
                    "ssl", {}
                )  # TLS certificate subject organizational unit
                .get("cert", {})
                .get("subject", {})
                .get("OU"),
                "subject_organisation": x.get(
                    "ssl", {}
                )  # TLS certificate subject organisation
                .get("cert", {})
                .get("subject", {})
                .get("O"),
                "subject_state": x.get("ssl", {})  # TLS certificate subject state
                .get("cert", {})
                .get("subject", {})
                .get("ST"),
                "subject_locality": x.get("ssl", {})  # TLS certificate subject locality
                .get("cert", {})
                .get("subject", {})
                .get("L"),
                "issuer_country": x.get("ssl", {})  # TLS certificate issuer country
                .get("cert", {})
                .get("issuer", {})
                .get("C"),
                "issuer_cn": x.get("ssl", {})  # TLS certificate issuer common name
                .get("cert", {})
                .get("issuer", {})
                .get("CN"),
                "issuer_ou": x.get(
                    "ssl", {}
                )  # TLS certificate issuer organizational unit
                .get("cert", {})
                .get("issuer", {})
                .get("OU"),
                "issuer_organisation": x.get(
                    "ssl", {}
                )  # TLS certificate issuer organisation
                .get("cert", {})
                .get("issuer", {})
                .get("O"),
                "issuer_state": x.get("ssl", {})  # TLS certificate issuer state
                .get("cert", {})
                .get("issuer", {})
                .get("ST"),
                "issuer_locality": x.get("ssl", {})  # TLS certificate issuer locality
                .get("cert", {})
                .get("issuer", {})
                .get("L"),
            }
            for x in data
        ]

        return pd.DataFrame.from_records(all_results)

    def _parse(self, input_data, private_namespace=None) -> tuple:
        node_dfs = {}
        rel_dfs = {}

        df = self._generate_df(input_data)

        #
        # Nodes
        #

        # IPs

        node_dfs[IPAddressNode.__primarylabel__] = df[["ip_address"]].copy()

        # Ports

        node_dfs[Port.__primarylabel__] = df[["port_number", "protocol"]].copy()

        # Listening Sockets

        sockets_df = df[["ip_address", "protocol", "port_number"]].copy()

        socket_ids = [
            ListeningSocket(**x).get_pp() for x in sockets_df.to_dict(orient="records")
        ]

        # Public IPs are unique
        sockets_df["ip_address_unique_id"] = sockets_df["ip_address"]

        # socket ID's are needed later for creating relationships
        df["socket_id"] = socket_ids

        node_dfs[ListeningSocket.__primarylabel__] = sockets_df

        # Certificates

        cert_full_df = df.loc[~df.sha1.isna()].copy()

        cert_df = cert_full_df[
            [
                "sha1",
                "sha256",
                "serial_number",
                "subject_country",
                "subject_cn",
                "subject_ou",
                "subject_organisation",
                "subject_state",
                "subject_locality",
                "issuer_country",
                "issuer_cn",
                "issuer_ou",
                "issuer_organisation",
                "issuer_state",
                "issuer_locality",
            ]
        ]

        node_dfs[X509Certificate.__primarylabel__] = cert_df

        # JARM Hashes

        jarm_full_df = df.loc[~df["jarm"].isna()].copy()
        jarm_df = jarm_full_df[["jarm"]].copy()

        node_dfs[JarmHash.__primarylabel__] = jarm_df

        # Banner

        banner_full_df = df.loc[~df["banner"].isna()].copy()
        banner_df = banner_full_df[["banner"]].copy()

        node_dfs[Banner.__primarylabel__] = banner_df

        #
        # Relationships
        #

        # IP to Socket

        ip_df = (
            sockets_df[["ip_address_unique_id"]]
            .rename(columns={"ip_address_unique_id": "source"})
            .copy()
        )

        socket_id_df = pd.DataFrame()
        socket_id_df["target"] = socket_ids

        rel_dfs[IPAddressHasOpenPort.__relationshiptype__] = {
            "src_df": ip_df.copy(),
            "tgt_df": socket_id_df.copy(),
        }

        # Socket to Ports

        port_df = pd.DataFrame()
        port_df["target"] = [
            Port(port_number=x["port_number"], protocol=x["protocol"]).get_pp()
            for x in sockets_df.to_dict(orient="records")
        ]

        rel_dfs[ListeningSocketUsesPort.__relationshiptype__] = {
            "src_df": socket_id_df.rename(columns={"target": "source"}).copy(),
            "tgt_df": port_df.copy(),
        }

        # Sockets to Banners

        banner_sha1_df = pd.DataFrame()
        banner_sha1_df["target"] = [
            Banner(banner=x["banner"]).get_pp()
            for x in banner_full_df.to_dict(orient="records")
        ]

        rel_dfs[ListeningSocketHasBanner.__relationshiptype__] = {
            "src_df": banner_full_df[["socket_id"]]
            .rename(columns={"socket_id": "source"})
            .copy(),
            "tgt_df": banner_sha1_df[["target"]].copy(),
        }

        # Sockets to Certificates

        cert_pp_df = pd.DataFrame()
        cert_pp_df["target"] = [
            X509Certificate(**x).get_pp() for x in cert_df.to_dict(orient="records")
        ]

        rel_dfs[ListeningSocketHasX509Certificate.__relationshiptype__] = {
            "src_df": cert_full_df[["socket_id"]]
            .rename(columns={"socket_id": "source"})
            .copy(),
            "tgt_df": cert_pp_df[["target"]].copy(),
        }

        # Sockets to JARMs

        rel_dfs[ListeningSocketHasJarmHash.__relationshiptype__] = {
            "src_df": jarm_full_df[["socket_id"]]
            .rename(columns={"socket_id": "source"})
            .copy(),
            "tgt_df": jarm_df[["jarm"]].copy(),
        }

        return node_dfs, rel_dfs


class ShodanOntolocyClient(OntolocyClient):
    def __init__(self):
        super().__init__()

        api_key = os.getenv("ONTOLOCY_SHODAN_KEY")

        self.client = shodan.Shodan(api_key)

        self.parser = ShodanParser()

    def _query(self, query):
        try:
            data = self.client.search(query)
        except shodan.APIError:
            raise

        return data


class ShodanIPEnricher(OntolocyEnricher):
    seed_type = SeedTypeEnum.IP

    def __init__(self):
        super().__init__()
        self.client = ShodanOntolocyClient()

    def _generate_single_query(self, seed):
        return f"ip:{seed}"

    def _generate_batch_query(self, seeds):
        return f"ip:{','.join(seeds)}"
