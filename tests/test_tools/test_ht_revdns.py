from ontolocy.tools.ht_revdns import (
    HackerTargetReverseDNSParser,
    HackerTargetReverseDNSClient,
    HackerTargetReverseDNSEnricher,
)

# Example reverse DNS data returned by the API for a domain lookup
test_data = """007.google.com,92.223.30.94
01sin.google.com,173.234.14.228
100-cache-blicnet.google.com,92.241.132.100
"""


def test_detect_ht_revdns():
    parser = HackerTargetReverseDNSParser()
    assert parser.detect(test_data) is True


def test_detect_ht_revdns_bad():
    parser = HackerTargetReverseDNSParser()
    bad_data = "not,a,valid,line"
    assert parser.detect(bad_data) is False


def test_node_parse_ht_revdns():
    parser = HackerTargetReverseDNSParser()
    ctx = {"query": "google.com"}
    parser.parse_data(test_data, ctx=ctx, populate=False)

    dnsrecord_df = parser.node_oriented_dfs["DNSRecord"]
    domain_df = parser.node_oriented_dfs["DomainName"]
    ip_df = parser.node_oriented_dfs["IPAddress"]

    assert len(dnsrecord_df.index) == 3
    assert len(domain_df.index) >= 3  # PTR domains + valid domains
    assert len(ip_df.index) == 3


def test_rel_parse_ht_revdns():
    parser = HackerTargetReverseDNSParser()
    ctx = {"query": "google.com"}
    parser.parse_data(test_data, ctx=ctx, populate=False)

    domain_to_dnsrecord_df = parser.rel_input_dfs["DOMAIN_NAME_HAS_DNS_RECORD"][
        "src_df"
    ]
    dnsrecord_to_ip_df = parser.rel_input_dfs["DNS_RECORD_POINTS_TO_IP_ADDRESS"][
        "src_df"
    ]
    dnsrecord_to_domain_df = parser.rel_input_dfs["DNS_RECORD_POINTS_TO_DOMAIN_NAME"][
        "src_df"
    ]

    assert len(domain_to_dnsrecord_df.index) == 3
    assert len(dnsrecord_to_ip_df.index) == 3
    assert len(dnsrecord_to_domain_df.index) >= 2  # Only valid domains matched


def test_populate_ht_revdns(use_graph):
    parser = HackerTargetReverseDNSParser()
    ctx = {"query": "google.com"}
    parser.parse_data(test_data, ctx=ctx, populate=True)

    cypher = """MATCH (d:DomainName)-[:DOMAIN_NAME_HAS_DNS_RECORD]->(r:DNSRecord)
                RETURN r"""
    assert len(use_graph.evaluate_query(cypher).nodes) == 3

    cypher = """MATCH (r:DNSRecord)-[:DNS_RECORD_POINTS_TO_IP_ADDRESS]->(i:IPAddress)
                RETURN i"""
    assert len(use_graph.evaluate_query(cypher).nodes) == 3


def test_client_query(monkeypatch):
    def mockreturn(self, query):
        return test_data

    monkeypatch.setattr(HackerTargetReverseDNSClient, "_query", mockreturn)
    client = HackerTargetReverseDNSClient()
    result = client._query("google.com")
    assert "007.google.com" in result


def test_enrich_domain_ht_revdns(monkeypatch, use_graph):
    def mockreturn(self, query):
        return test_data

    monkeypatch.setattr(HackerTargetReverseDNSClient, "_query", mockreturn)
    enricher = HackerTargetReverseDNSEnricher()
    enricher.enrich("google.com")

    cypher = """MATCH (d:DomainName)-[:DOMAIN_NAME_HAS_DNS_RECORD]->(r:DNSRecord)
                RETURN r"""
    assert len(use_graph.evaluate_query(cypher).nodes) == 3
