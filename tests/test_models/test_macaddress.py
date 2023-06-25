import pytest

from ontolocy import MACAddress, Host, MACAddressAssignedToHost


@pytest.mark.parametrize(
    "input,formatted",
    [
        ("01:02:03:04:ab:cd", "01:02:03:04:AB:CD"),
        ("01-02-03-04-ab-cd", "01:02:03:04:AB:CD"),
        ("01:02:03:04:AB:CD", "01:02:03:04:AB:CD"),
    ],
)
def test_mac(input, formatted):

    mac = MACAddress(mac_address=input)

    assert mac.get_identifier() == formatted


def test_mac_address_assigned_to_host(use_graph):

    mac = MACAddress(mac_address="01:02:03:04:AB:CD")
    mac.merge()

    host = Host(hostname="TestHost1")
    host.merge()

    rel = MACAddressAssignedToHost(source=mac, target=host)
    rel.merge()

    cypher = """
    MATCH (mac:MACAddress)-[:MAC_ADDRESS_ASSIGNED_TO_HOST]->(host:Host)
    WHERE mac.mac_address = "01:02:03:04:AB:CD"
    RETURN COUNT(DISTINCT host)
    """

    result = use_graph.evaluate(cypher)

    assert result == 1
