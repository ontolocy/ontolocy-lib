import re

import pandas as pd
import requests

from ontolocy import (
    DNSRecord,
    DNSRecordPointsToDomainName,
    DNSRecordPointsToIPAddress,
    DomainName,
    DomainNameHasDNSRecord,
    IPAddressNode,
)

from .ontolocy_enricher import (
    SEED_MAPPINGS,
    OntolocyClient,
    OntolocyEnricher,
    SeedTypeEnum,
)
from .ontolocy_parser import OntolocyParser


def reverse_ip(ip):
    """Reverse the octets of an IPv4 address for PTR record naming."""
    return ".".join(ip.split(".")[::-1])


class HackerTargetSubdomainParser(OntolocyParser):
    """
    Parser for HackerTarget subdomain enumeration endpoint.

    See https://hackertarget.com/find-dns-host-records/
    """

    node_types = [DNSRecord, DomainName, IPAddressNode]
    rel_types = [
        DNSRecordPointsToDomainName,
        DNSRecordPointsToIPAddress,
        DomainNameHasDNSRecord,
    ]

    def _detect(self, input_data: str) -> bool:
        # expects new line separated entries of "domain,ip"
        for line in input_data.splitlines():
            parts = line.split(",")
            if len(parts) != 2:
                return False
            ip_part = parts[1]
            if not re.search(SEED_MAPPINGS["ip"]["pattern"], ip_part):
                return False
        return True

    def _parse(self, input_data, private_namespace, ctx):
        """
        Parse the data.

        Expects ctx to be a dictionary with a 'query' key for the domain name queried.
        """
        records = []
        domains = []
        ips = []
        domain_to_dnsrecord_rels = []
        dnsrecord_to_ip_rels = []
        dnsrecord_to_domain_rels = []

        for line in input_data.splitlines():
            parts = line.split(",")
            domain_part = parts[0]
            ip_part = parts[1]

            # PTR record name: reversed IP + .in-addr.arpa.
            ptr_name = f"{reverse_ip(ip_part)}.in-addr.arpa."

            record = {
                "type": "PTR",
                "name": ptr_name,
                "content": domain_part,
            }
            records.append(record)
            record_id = DNSRecord(**record).unique_id

            ips.append({"ip_address": ip_part})

            dnsrecord_to_ip_rels.append({"source": record_id, "target": ip_part})

            # Only create DomainName node and relationship if not a wildcard
            if re.match(SEED_MAPPINGS["domain"]["pattern"], domain_part):
                domains.append({"name": domain_part})
                dnsrecord_to_domain_rels.append(
                    {"source": record_id, "target": domain_part}
                )

            # Always create DomainName node for PTR domain and relationship
            ptr_domain = ptr_name.rstrip(".")
            domains.append({"name": ptr_domain})
            domain_to_dnsrecord_rels.append({"source": ptr_domain, "target": record_id})

        node_dfs = {
            DNSRecord.__primarylabel__: pd.DataFrame.from_records(records)
            .drop_duplicates()
            .reset_index(drop=True),
            DomainName.__primarylabel__: pd.DataFrame.from_records(domains)
            .drop_duplicates()
            .reset_index(drop=True),
            IPAddressNode.__primarylabel__: pd.DataFrame.from_records(ips)
            .drop_duplicates()
            .reset_index(drop=True),
        }

        rel_dfs = {
            DomainNameHasDNSRecord.__relationshiptype__: {
                "src_df": pd.DataFrame.from_records(domain_to_dnsrecord_rels)[
                    ["source"]
                ].copy(),
                "tgt_df": pd.DataFrame.from_records(domain_to_dnsrecord_rels)[
                    ["target"]
                ].copy(),
            },
            DNSRecordPointsToIPAddress.__relationshiptype__: {
                "src_df": pd.DataFrame.from_records(dnsrecord_to_ip_rels)[
                    ["source"]
                ].copy(),
                "tgt_df": pd.DataFrame.from_records(dnsrecord_to_ip_rels)[
                    ["target"]
                ].copy(),
            },
            DNSRecordPointsToDomainName.__relationshiptype__: {
                "src_df": pd.DataFrame.from_records(dnsrecord_to_domain_rels)[
                    ["source"]
                ].copy(),
                "tgt_df": pd.DataFrame.from_records(dnsrecord_to_domain_rels)[
                    ["target"]
                ].copy(),
            },
        }

        return node_dfs, rel_dfs


class HackerTargetSubdomainClient(OntolocyClient):
    """Client for querying the HackerTarget subdomain endpoint."""

    def __init__(self):
        super().__init__()
        self.parser = HackerTargetSubdomainParser()

    def _query(self, query: str):
        """Query the HackerTarget subdomain API.

        Args:
            query (str): domain name to lookup
        """
        api_endpoint = "https://api.hackertarget.com/hostsearch/"
        response = requests.get(api_endpoint, params={"q": query})
        response.raise_for_status()
        return response.text


class HackerTargetSubdomainEnricher(OntolocyEnricher):
    seed_type = SeedTypeEnum.DOMAIN

    def __init__(self):
        super().__init__()
        self.client = HackerTargetSubdomainClient()

    def _generate_single_query(self, seed):
        return seed
