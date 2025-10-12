import json

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

from .ontolocy_enricher import OntolocyClient, OntolocyEnricher, SeedTypeEnum
from .ontolocy_parser import OntolocyParser


class HackerTargetDNSParser(OntolocyParser):
    """Parser for HackerTarget DNS lookup data.

    See https://hackertarget.com/dns-lookup/ for more details.
    """

    node_types = [DNSRecord, DomainName, IPAddressNode]

    rel_types = [
        DNSRecordPointsToDomainName,
        DNSRecordPointsToIPAddress,
        DomainNameHasDNSRecord,
    ]

    def _detect(self, input_data) -> bool:
        if not isinstance(input_data, dict):
            return False

        for key in input_data.keys():
            if key not in ["A", "AAAA", "CNAME", "MX", "NS", "SOA", "TXT", "PTR"]:
                return False

        return True

    def _load_data(self, raw_data):
        return json.loads(raw_data)

    def _parse(self, input_data, private_namespace, ctx):
        """
        Parse the data.

        Expects ctx to be a dictionary with a 'domain' key for the domain name queried.

        """

        # create complete individual records

        records = []
        domains = []
        ips = []
        domain_to_dnsrecord_rels = []
        dnsrecord_to_ip_rels = []
        dnsrecord_to_domain_rels = []

        domain_name = ctx["query"]

        domains.append({"name": domain_name})

        for record_type, content in input_data.items():
            for entry in content:
                record = {
                    "type": record_type,
                    "name": domain_name,
                    "content": entry,
                }

                records.append(record)

                record_id = DNSRecord(
                    type=record_type,
                    name=domain_name,
                    content=entry,
                ).unique_id

                domain_to_dnsrecord_rels.append(
                    {"source": domain_name, "target": record_id}
                )

                if record_type in ["A", "AAAA"]:
                    ips.append({"ip_address": entry})
                    dnsrecord_to_ip_rels.append({"source": record_id, "target": entry})

                elif record_type in ["CNAME", "NS", "PTR"]:
                    target_domain = entry.rstrip(".")
                    domains.append({"name": target_domain})
                    dnsrecord_to_domain_rels.append(
                        {"source": record_id, "target": target_domain}
                    )

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


class HackerTargetDNSClient(OntolocyClient):
    """Lightweight client for querying the HackerTarget DNS lookup API.

    See https://hackertarget.com/dns-lookup/ for more details.

    Query method expects a domain name as input.
    """

    def __init__(self):
        super().__init__()
        self.parser = HackerTargetDNSParser()

    def _query(self, query: str):
        """Query the HackerTarget DNS lookup API.

        Args:
            query (str): domain name to lookup
        """

        api_endpoint = "https://api.hackertarget.com/dnslookup/"

        response = requests.get(api_endpoint, params={"q": query, "output": "json"})

        # raise an exception for bad responses
        response.raise_for_status()

        return response.json()


class HackerTargetDNSEnricher(OntolocyEnricher):
    seed_type = SeedTypeEnum.DOMAIN

    def __init__(self):
        super().__init__()
        self.client = HackerTargetDNSClient()

    def _generate_single_query(self, seed):
        return seed
