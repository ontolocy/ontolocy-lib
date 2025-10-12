import json

from ontolocy.tools.ht_dns import (
    HackerTargetDNSParser,
    HackerTargetDNSEnricher,
    HackerTargetDNSClient,
)


test_data = """{
  "A": [
    "23.192.228.80",
    "23.220.75.232",
    "23.215.0.136",
    "23.220.75.245",
    "23.215.0.138",
    "23.192.228.84"
  ],
  "AAAA": [
    "2600:1408:ec00:36::1736:7f24",
    "2600:1406:bc00:53::b81e:94c8",
    "2600:1406:bc00:53::b81e:94ce",
    "2600:1406:5e00:6::17ce:bc1b",
    "2600:1408:ec00:36::1736:7f31",
    "2600:1406:5e00:6::17ce:bc12"
  ],
  "MX": [
    "0 ."
  ],
  "NS": [
    "b.iana-servers.net.",
    "a.iana-servers.net."
  ],
  "TXT": [
    "v=spf1 -all",
    "_k2n1y4vw3qtb4skdx9e7dxt97qrmmq9"
  ],
  "CNAME": [],
  "SOA": [
    "ns.icann.org. noc.dns.icann.org. 2025082219 7200 3600 1209600 3600"
  ]
}"""


def test_detect_ht_dns():
    parser = HackerTargetDNSParser()

    input_data = parser._load_data(test_data)

    assert parser.detect(input_data) is True


def test_detect_ht_dns_bad():
    parser = HackerTargetDNSParser()

    assert parser.detect("incorrect") is False


def test_node_parse_ht_dns():
    parser = HackerTargetDNSParser()

    input_data = parser._load_data(test_data)
    ctx = {"query": "example.com"}
    parser.parse_data(input_data, ctx=ctx, populate=False)

    dnsrecord_df = parser.node_oriented_dfs["DNSRecord"]

    assert len(dnsrecord_df.index) == 18

    domain_df = parser.node_oriented_dfs["DomainName"]

    assert len(domain_df.index) == 3
    assert domain_df.iloc[0]["name"] == "example.com"

    ip_df = parser.node_oriented_dfs["IPAddress"]

    assert len(ip_df.index) == 12


def test_rel_parse_ht_dns():
    parser = HackerTargetDNSParser()

    input_data = parser._load_data(test_data)
    ctx = {"query": "example.com"}
    parser.parse_data(input_data, ctx=ctx, populate=False)

    domain_to_dnsrecord_df = parser.rel_input_dfs["DOMAIN_NAME_HAS_DNS_RECORD"][
        "src_df"
    ]
    assert len(domain_to_dnsrecord_df.index) == 18

    dnsrecord_to_ip_df = parser.rel_input_dfs["DNS_RECORD_POINTS_TO_IP_ADDRESS"][
        "src_df"
    ]
    assert len(dnsrecord_to_ip_df.index) == 12

    dnsrecord_to_domain_df = parser.rel_input_dfs["DNS_RECORD_POINTS_TO_DOMAIN_NAME"][
        "src_df"
    ]
    assert len(dnsrecord_to_domain_df.index) == 2


def test_populate_ht_dns(use_graph):
    parser = HackerTargetDNSParser()

    input_data = parser._load_data(test_data)
    ctx = {"query": "example.com"}
    parser.parse_data(input_data, ctx=ctx, populate=True)

    cypher = """MATCH (d:DomainName)-[:DOMAIN_NAME_HAS_DNS_RECORD]->(r:DNSRecord)
                WHERE d.name = "example.com"
                RETURN r"""
    assert len(use_graph.evaluate_query(cypher).nodes) == 18

    cypher = """MATCH (r:DNSRecord)-[:DNS_RECORD_POINTS_TO_IP_ADDRESS]->(i:IPAddress)
                WHERE r.name = "example.com"
                RETURN i"""
    assert len(use_graph.evaluate_query(cypher).nodes) == 12

    cypher = """MATCH (r:DNSRecord)-[:DNS_RECORD_POINTS_TO_DOMAIN_NAME]->(d:DomainName)
                WHERE r.name = "example.com"
                RETURN r"""
    assert len(use_graph.evaluate_query(cypher).nodes) == 2


def test_enrich_domain_ht_dns(monkeypatch, use_graph):
    def mockreturn(self, query):
        return json.loads(test_data)

    monkeypatch.setattr(HackerTargetDNSClient, "_query", mockreturn)

    enricher = HackerTargetDNSEnricher()
    enricher.enrich("example.com")

    cypher = """MATCH (d:DomainName)-[:DOMAIN_NAME_HAS_DNS_RECORD]->(r:DNSRecord)
                WHERE d.name = "example.com"
                RETURN r"""
    assert len(use_graph.evaluate_query(cypher).nodes) == 18
