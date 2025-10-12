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


class HackerTargetPtrIPParser(OntolocyParser):
    """Parser for HackerTarget reverse DNS lookup by IP.

    This endpoint actively resolves reverse DNS (PTR) records for given IP addresses.

    See https://hackertarget.com/reverse-dns-lookup/ for more details.
    """

    node_types = [DNSRecord, DomainName, IPAddressNode]

    rel_types = [
        DNSRecordPointsToDomainName,
        DNSRecordPointsToIPAddress,
        DomainNameHasDNSRecord,
    ]

    def _detect(self, input_data: str) -> bool:
        # expects  new line separated entries of "IP DOMAIN"
        for line in input_data.splitlines():
            parts = line.split()
            if len(parts) != 2:
                return False

            ip_part = parts[0]

            if not re.search(SEED_MAPPINGS["ip"]["pattern"], ip_part):
                return False

        return True

    def _parse(self, input_data, private_namespace, ctx):
        """
        Parse the data.

        Expects ctx to be a dictionary with a 'domain' key for the domain name queried.

        """

        records = []
        domains = []
        ips = []
        domain_to_dnsrecord_rels = []
        dnsrecord_to_ip_rels = []
        dnsrecord_to_domain_rels = []

        for line in input_data.splitlines():
            parts = line.split()
            ip_part = parts[0]
            domain_part = parts[1]

            record_name = f"{ip_part}.in-addr.arpa."

            ptr_domain = record_name.rstrip(".")

            domains.append({"name": ptr_domain})

            record = {
                "type": "PTR",
                "name": record_name,
                "content": domain_part,
            }

            records.append(record)

            record_id = DNSRecord(**record).unique_id

            ips.append({"ip_address": ip_part})

            dnsrecord_to_ip_rels.append({"source": record_id, "target": ip_part})

            domain_to_dnsrecord_rels.append({"source": ptr_domain, "target": record_id})

            # entries may be wildcards rather than explicit domain names
            if re.match(SEED_MAPPINGS["domain"]["pattern"], domain_part):
                domains.append({"name": domain_part})

                dnsrecord_to_domain_rels.append(
                    {"source": record_id, "target": domain_part}
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


class HackerTargetPtrIPClient(OntolocyClient):
    """Lightweight client for querying the HackerTarget DNS lookup API.

    See https://hackertarget.com/dns-lookup/ for more details.

    Query method expects a domain name as input.
    """

    def __init__(self):
        super().__init__()
        self.parser = HackerTargetPtrIPParser()

    def _query(self, query: str):
        """Query the HackerTarget Reverse DNS lookup API.

        Args:
            query (str): domain name to lookup
        """

        api_endpoint = "https://api.hackertarget.com/reversedns/"

        response = requests.get(api_endpoint, params={"q": query})

        # raise an exception for bad responses
        response.raise_for_status()

        return response.text


class HackerTargetPtrIPEnricher(OntolocyEnricher):
    seed_type = SeedTypeEnum.IP

    def __init__(self):
        super().__init__()
        self.client = HackerTargetPtrIPClient()

    def _generate_single_query(self, seed):
        return seed
