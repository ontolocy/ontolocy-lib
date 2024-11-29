from ipaddress import IPv4Address
import pandas as pd
import pytest

from ontolocy import (
    IPAddressNode,
    Country,
    DataOrigin,
    ListeningSocket,
    IPAddressHasOpenPort,
    IPAddressBelongsToASN,
    IPAddressLocatedInCountry,
    ASN,
)


@pytest.mark.parametrize(
    "ip_address,private,version",
    [
        ("1.1.1.1", False, "ipv4"),
        ("8.8.8.8", False, "ipv4"),
        ("192.168.101.123", True, "ipv4"),
        ("10.4.5.6", True, "ipv4"),
        ("2001:db8::1", True, "ipv6"),
        ("2001:4860:4860::8888", False, "ipv6"),
    ],
)
def test_basic_ips(ip_address, private, version):
    ip = IPAddressNode(ip_address=ip_address)

    assert ip.private is private
    assert ip.ip_version == version
    assert str(ip) == ip_address

    if private:
        assert ip.namespace is not None

    else:
        assert ip.namespace is None


@pytest.mark.parametrize(
    "ip_address,unique_id",
    [
        ("1.1.1.1", "1.1.1.1"),
        ("8.8.8.8", "8.8.8.8"),
        ("2001:4860:4860::8888", "2001:4860:4860::8888"),
    ],
)
def test_repeatable_unique_id_public(ip_address, unique_id):
    ip1 = IPAddressNode(ip_address=ip_address, namespace="this shouldn't matter")

    uuid1 = ip1.unique_id

    ip2 = IPAddressNode(ip_address=ip_address)

    uuid2 = ip2.unique_id

    assert uuid1 == uuid2

    assert uuid1 == unique_id


def test_repeatable_unique_id_private():
    ip1 = IPAddressNode(ip_address="192.168.0.1", namespace="ontolocy-test")

    uuid1 = ip1.unique_id

    ip2 = IPAddressNode(ip_address="192.168.0.1", namespace="ontolocy-test")

    uuid2 = ip2.unique_id

    assert uuid1 == uuid2

    assert uuid1 == "9ec0a0fc-1fc5-50b1-925c-db5393faf934"


def test_unique_id_private():
    ip1 = IPAddressNode(ip_address="192.168.0.1")

    uuid1 = ip1.unique_id

    ip2 = IPAddressNode(ip_address="192.168.0.1")

    uuid2 = ip2.unique_id

    assert uuid1 != uuid2


def test_unique_id_public():
    ip1 = IPAddressNode(ip_address="1.1.1.1")

    assert ip1.unique_id == "1.1.1.1"


def test_ingest_df(use_graph):
    my_ips = [
        {
            "ip_address": "192.168.10.1",
            "namespace": "ontolocy-test",
        },
        {
            "ip_address": "192.168.10.2",
            "namespace": "ontolocy-test",
        },
    ]

    my_ips_df = pd.DataFrame.from_records(my_ips)

    data_origin = DataOrigin(name="Ontolocy Test Data")

    IPAddressNode.ingest_df(my_ips_df, data_origin)

    cypher = """
    MATCH (o:DataOrigin)-[:ORIGIN_GENERATED]->(ip:IPAddress)
    WHERE o.name = 'Ontolocy Test Data'
    RETURN COUNT(DISTINCT ip)
    """

    result = use_graph.evaluate_query_single(cypher)

    assert result == 2


def test_merge_df(use_graph):
    my_ips = [
        {
            "ip_address": "192.168.10.1",
            "namespace": "ontolocy-test",
        },
        {
            "ip_address": "192.168.10.1",
            "namespace": "ontolocy-test",
        },
        {
            "ip_address": "192.168.10.2",
            "namespace": "ontolocy-test",
        },
        {
            "ip_address": "1.1.1.1",
            "namespace": "ontolocy-test",
        },
        {
            "ip_address": "8.8.8.8",
            "namespace": "ontolocy-test",
        },
        {
            "ip_address": "8.8.8.8",
            "namespace": "ontolocy-test",
        },
        {
            "ip_address": "2001:4860:4860::8888",
            "namespace": "ontolocy-test",
        },
        {
            "ip_address": "2001:db8::1",
            "namespace": "ontolocy-test",
        },
        {
            "ip_address": "2001:db8::1",
            "namespace": "ontolocy-test",
        },
    ]

    my_ips_df = pd.DataFrame.from_records(my_ips)

    # merge_df should give us back a list of results which reflects the shape of the data sent in
    merge_results = IPAddressNode.merge_df(my_ips_df)

    assert len(merge_results) == len(my_ips_df)

    assert merge_results[0].ip_address == IPv4Address("192.168.10.1")
    assert merge_results[0].private is True
    assert merge_results[0].ip_version == "ipv4"

    assert merge_results[3].ip_address == IPv4Address("1.1.1.1")
    assert merge_results[3].private is False
    assert merge_results[3].ip_version == "ipv4"

    # we shouldn't have created any duplicate nodes because of the namespacing
    # therefore if we just match all nodes, we should only get 6 hits

    match_results = IPAddressNode.match_nodes()

    assert len(match_results) == 6


def test_ip_address_has_open_port(use_graph):
    ip = IPAddressNode(ip_address="8.8.8.8")
    ip.merge()

    socket = ListeningSocket(ip_address="8.8.8.8", protocol="udp", port_number=53)
    socket.merge()

    rel = IPAddressHasOpenPort(source=ip, target=socket)
    rel.merge()

    cypher = """
    MATCH (ip:IPAddress)-[:IP_ADDRESS_HAS_OPEN_PORT]->(op:ListeningSocket)
    WHERE ip.ip_address = '8.8.8.8'
    RETURN COUNT(DISTINCT op)
    """

    result = use_graph.evaluate_query_single(cypher)

    assert result == 1


def test_ip_address_belongs_to_asn(use_graph):
    ip = IPAddressNode(ip_address="8.8.8.8")
    ip.merge()

    asn = ASN(
        number=15169,
        country_code="US",
        registry="arin",
        network_name="GOOGLE",
        description="GOOGLE - Google Inc., US",
        cidr="8.8.8.0/24",
    )
    asn.merge()

    rel = IPAddressBelongsToASN(source=ip, target=asn)
    rel.merge()

    cypher = """
    MATCH (ip:IPAddress)-[:IP_ADDRESS_BELONGS_TO_ASN]->(asn:ASN)
    WHERE ip.ip_address = '8.8.8.8'
    RETURN COUNT(DISTINCT asn)
    """

    result = use_graph.evaluate_query_single(cypher)

    assert result == 1


def test_ip_address_located_in_country(use_graph):
    ip = IPAddressNode(ip_address="8.8.8.8")
    ip.merge()

    country = Country(country_code="DE")
    country.merge()

    rel = IPAddressLocatedInCountry(source=ip, target=country)
    rel.merge()

    cypher = """
    MATCH (ip:IPAddress)-[:IP_ADDRESS_LOCATED_IN_COUNTRY]->(country:Country)
    WHERE ip.ip_address = '8.8.8.8'
    RETURN COUNT(DISTINCT country)
    """

    result = use_graph.evaluate_query_single(cypher)

    assert result == 1
