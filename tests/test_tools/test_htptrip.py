from ontolocy import DomainName, IPAddressNode

from ontolocy.tools.ht_ptrip import (
    HackerTargetPtrIPParser,
    HackerTargetPtrIPClient,
    HackerTargetPtrIPEnricher,
)

test_data = "1.1.1.1 one.one.one.one"


def test_detect_ht_ptrip():
    parser = HackerTargetPtrIPParser()

    input_data = parser._load_data(test_data)

    assert parser.detect(input_data) is True


def test_detect_ht_ptrip_bad():
    parser = HackerTargetPtrIPParser()

    assert parser.detect("incorrect") is False


def test_node_parse_ht_ptrip():

    parser = HackerTargetPtrIPParser()

    parser.parse_data(test_data, populate=False)

    dnsrecord_df = parser.node_oriented_dfs["DNSRecord"]
    assert len(dnsrecord_df.index) == 1

    assert dnsrecord_df.iloc[0]["name"] == "1.1.1.1.in-addr.arpa."

    domain_df = parser.node_oriented_dfs["DomainName"]
    assert len(domain_df.index) == 2

    ip_df = parser.node_oriented_dfs["IPAddress"]
    assert len(ip_df.index) == 1


def test_rel_parse_ht_ptrip():
    parser = HackerTargetPtrIPParser()

    parser.parse_data(test_data, populate=False)

    domain_to_dnsrecord_df = parser.rel_input_dfs["DOMAIN_NAME_HAS_DNS_RECORD"][
        "src_df"
    ]
    assert len(domain_to_dnsrecord_df.index) == 1

    dnsrecord_to_ip_df = parser.rel_input_dfs["DNS_RECORD_POINTS_TO_IP_ADDRESS"][
        "src_df"
    ]
    assert len(dnsrecord_to_ip_df.index) == 1

    dnsrecord_to_domain_df = parser.rel_input_dfs["DNS_RECORD_POINTS_TO_DOMAIN_NAME"][
        "src_df"
    ]
    assert len(dnsrecord_to_domain_df.index) == 1


def test_populate_ht_ptrip(use_graph):
    parser = HackerTargetPtrIPParser()

    parser.parse_data(test_data, populate=True)

    assert DomainName.get_count() == 2

    cypher = """MATCH (d:DomainName)-[:DOMAIN_NAME_HAS_DNS_RECORD]->(r:DNSRecord)
                WHERE d.name = "1.1.1.1.in-addr.arpa"
                RETURN r"""
    assert len(use_graph.evaluate_query(cypher).nodes) == 1

    cypher = """MATCH (r:DNSRecord)-[:DNS_RECORD_POINTS_TO_IP_ADDRESS]->(i:IPAddress)
                WHERE i.ip_address = "1.1.1.1"
                RETURN i"""
    assert len(use_graph.evaluate_query(cypher).nodes) == 1

    cypher = """MATCH (r:DNSRecord)-[:DNS_RECORD_POINTS_TO_DOMAIN_NAME]->(d:DomainName)
                WHERE d.name = "one.one.one.one"
                RETURN r"""
    assert len(use_graph.evaluate_query(cypher).nodes) == 1


def test_enrich_ip_ht_ptrip(monkeypatch, use_graph):
    def mockreturn(self, query):
        return test_data

    monkeypatch.setattr(HackerTargetPtrIPClient, "_query", mockreturn)

    enricher = HackerTargetPtrIPEnricher()
    enricher.enrich("1.1.1.1")

    assert IPAddressNode.match("1.1.1.1")
