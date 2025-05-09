from uuid import UUID

from ontolocy import (
    IPAddressNode,
    ListeningSocket,
    ListeningSocketHostsURL,
    ListeningSocketUsesPort,
    Port,
    URLNode,
)


def test_define_socket():
    my_sock = ListeningSocket(
        ip_address="192.168.10.101", port_number=22, protocol="tcp"
    )

    assert my_sock.port_number == 22
    assert isinstance(my_sock.unique_id, str)
    assert str(my_sock) == "192.168.10.101:22 (tcp)"


def test_define_socket_same_unique_id():
    expected_uuid = UUID("ff918cef-f63c-5850-8d6b-f73c623b4c2e")

    my_sock_1 = ListeningSocket(
        ip_address="192.168.10.101", port_number=22, protocol="tcp", namespace="TESTING"
    )
    my_sock_2 = ListeningSocket(
        ip_address="192.168.10.101", port_number=22, protocol="tcp", namespace="TESTING"
    )

    assert my_sock_1.unique_id == my_sock_2.unique_id

    assert my_sock_1.unique_id == str(expected_uuid)


def test_define_socket_different_unique_id():
    my_sock_1 = ListeningSocket(
        ip_address="192.168.10.101", port_number=53, protocol="tcp", namespace="TESTING"
    )
    my_sock_2 = ListeningSocket(
        ip_address="192.168.10.101", port_number=53, protocol="udp", namespace="TESTING"
    )

    assert my_sock_1.unique_id != my_sock_2.unique_id


def test_define_socket_ip_unique_id_public():
    """Test that we generate a unique id for the IP which matches an IP generated unique id"""

    sock = ListeningSocket(ip_address="1.1.1.1", port_number=53, protocol="tcp")
    ip = IPAddressNode(ip_address="1.1.1.1")

    assert sock.ip_address_unique_id == ip.unique_id


def test_define_socket_ip_unique_id_private():
    """Test that we generate a unique id for the IP which matches an IP generated unique id"""

    sock = ListeningSocket(
        ip_address="192.168.1.101", port_number=53, protocol="tcp", namespace="TESTING"
    )
    ip = IPAddressNode(ip_address="192.168.1.101", namespace="TESTING")

    assert sock.ip_address_unique_id == ip.unique_id


def test_define_socket_ip_unique_id_private_different():
    """Test that we generate a unique id for the IP which matches an IP generated unique id"""

    sock = ListeningSocket(ip_address="192.168.1.101", port_number=53, protocol="tcp")
    ip = IPAddressNode(ip_address="192.168.1.101")

    assert sock.ip_address_unique_id != ip.unique_id


def test_listening_socket_uses_port(use_graph):
    port = Port(port_number=53, protocol="udp")
    port.merge()

    socket = ListeningSocket(ip_address="8.8.8.8", protocol="udp", port_number=53)
    socket.merge()

    rel = ListeningSocketUsesPort(source=socket, target=port)
    rel.merge()

    cypher = """
    MATCH (sock:ListeningSocket)-[r:LISTENING_SOCKET_USES_PORT]->(port:Port)
    WHERE sock.unique_id = $socket_id
    RETURN COUNT(DISTINCT r)
    """

    params = {"socket_id": socket.get_pp()}

    result = use_graph.evaluate_query_single(cypher, params)

    assert result == 1


def test_listening_socket_has_url(use_graph):
    socket = ListeningSocket(ip_address="8.8.8.8", protocol="udp", port_number=53)
    socket.merge()

    url = URLNode(url="http://example.com/foo")
    url.merge()

    rel = ListeningSocketHostsURL(source=socket, target=url)
    rel.merge()

    cypher = """
    MATCH (sock:ListeningSocket)-[r:LISTENING_SOCKET_HOSTS_URL]->(url:URL)
    WHERE sock.unique_id = $socket_id
    RETURN COUNT(DISTINCT r)
    """

    params = {"socket_id": socket.get_pp()}

    result = use_graph.evaluate_query_single(cypher, params)

    assert result == 1
