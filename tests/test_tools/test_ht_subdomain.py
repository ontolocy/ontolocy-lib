from ontolocy.tools.ht_subdomain import (
    HackerTargetSubdomainParser,
    HackerTargetSubdomainClient,
    HackerTargetSubdomainEnricher,
)

# Example output from the API (comma separated domain,ip pairs)
test_data = """google.com,142.251.184.102
*.evenflow-test.adz.google.com,173.194.65.129
accounts.google.com,74.125.137.84
"""


def test_detect_ht_subdomain():
    parser = HackerTargetSubdomainParser()
    assert parser.detect(test_data) is True


def test_detect_ht_subdomain_bad():
    parser = HackerTargetSubdomainParser()
    bad_data = "not,a,valid,line"
    assert parser.detect(bad_data) is False


def test_node_parse_ht_subdomain():
    parser = HackerTargetSubdomainParser()
    ctx = {"query": "google.com"}
    parser.parse_data(test_data, ctx=ctx, populate=False)

    dnsrecord_df = parser.node_oriented_dfs["DNSRecord"]
    domain_df = parser.node_oriented_dfs["DomainName"]
    ip_df = parser.node_oriented_dfs["IPAddress"]

    # 3 records, 2 non-wildcard domains, 3 PTR domains, 3 IPs
    assert len(dnsrecord_df.index) == 3
    assert "google.com" in domain_df["name"].values
    assert "accounts.google.com" in domain_df["name"].values
    assert "*.evenflow-test.adz.google.com" not in domain_df["name"].values
    assert len(ip_df.index) == 3


def test_rel_parse_ht_subdomain():
    parser = HackerTargetSubdomainParser()
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

    # 3 PTR domains, 3 records, 2 record->domain relationships (no wildcard)
    assert len(domain_to_dnsrecord_df.index) == 3
    assert len(dnsrecord_to_ip_df.index) == 3
    assert len(dnsrecord_to_domain_df.index) == 2


def test_populate_ht_subdomain(use_graph):
    parser = HackerTargetSubdomainParser()
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

    monkeypatch.setattr(HackerTargetSubdomainClient, "_query", mockreturn)
    client = HackerTargetSubdomainClient()
    result = client._query("google.com")
    assert "google.com" in result


def test_enrich_domain_ht_subdomain(monkeypatch, use_graph):
    def mockreturn(self, query):
        return test_data

    monkeypatch.setattr(HackerTargetSubdomainClient, "_query", mockreturn)
    enricher = HackerTargetSubdomainEnricher()
    enricher.enrich("google.com")

    cypher = """MATCH (d:DomainName)-[:DOMAIN_NAME_HAS_DNS_RECORD]->(r:DNSRecord)
                RETURN r"""
    assert len(use_graph.evaluate_query(cypher).nodes) == 3
