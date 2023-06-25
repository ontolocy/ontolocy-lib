from uuid import UUID

from ontolocy import (
    ListeningSocket,
    Port,
    ListeningSocketUsesPort,
    ServiceHostsURL,
    URLNode,
)


def test_define_socket():

    my_sock = ListeningSocket(
        ip_address="192.168.10.101", port_number=22, protocol="tcp"
    )

    assert my_sock.port_number == 22
    assert isinstance(my_sock.unique_id, UUID)
    assert my_sock.get_identifier() == "192.168.10.101:22"


def test_define_socket_same_unique_id():

    expected_uuid = UUID("07ad6db1-3d75-5e4f-8fdc-596a8b57489a")

    my_sock_1 = ListeningSocket(
        ip_address="192.168.10.101", port_number=22, protocol="tcp"
    )
    my_sock_2 = ListeningSocket(
        ip_address="192.168.10.101", port_number=22, protocol="tcp"
    )

    assert my_sock_1.unique_id == my_sock_2.unique_id

    assert my_sock_1.unique_id == expected_uuid


def test_define_socket_different_unique_id():

    my_sock_1 = ListeningSocket(
        ip_address="192.168.10.101", port_number=53, protocol="tcp"
    )
    my_sock_2 = ListeningSocket(
        ip_address="192.168.10.101", port_number=53, protocol="udp"
    )

    assert my_sock_1.unique_id != my_sock_2.unique_id


def test_listening_socket_uses_port(use_graph):

    port = Port(port_number=53, protocol="udp")
    port.merge()

    socket = ListeningSocket(ip_address="8.8.8.8", protocol="udp", port_number=53)
    socket.merge()

    rel = ListeningSocketUsesPort(source=socket, target=port)
    rel.merge()

    cypher = f"""
    MATCH (sock:ListeningSocket)-[r:LISTENING_SOCKET_USES_PORT]->(port:Port)
    WHERE sock.unique_id = $socket_id
    RETURN COUNT(DISTINCT r)
    """

    params = {"socket_id": socket.get_primary_property_value()}

    result = use_graph.evaluate(cypher, params)

    assert result == 1


def test_listening_socket_has_url(use_graph):

    socket = ListeningSocket(ip_address="8.8.8.8", protocol="udp", port_number=53)
    socket.merge()

    url = URLNode(url="http://example.com/foo")
    url.merge()

    rel = ServiceHostsURL(source=socket, target=url)
    rel.merge()

    cypher = f"""
    MATCH (sock:ListeningSocket)-[r:SERVICE_HOSTS_URL]->(url:URL)
    WHERE sock.unique_id = $socket_id
    RETURN COUNT(DISTINCT r)
    """

    params = {"socket_id": socket.get_primary_property_value()}

    result = use_graph.evaluate(cypher, params)

    assert result == 1
