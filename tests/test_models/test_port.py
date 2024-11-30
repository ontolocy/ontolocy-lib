import pytest

from ontolocy import Port


@pytest.mark.parametrize(
    "port_number,protocol,unique_id, port_str",
    [
        (80, "tcp", "227d6eb4-4125-5e49-b6b0-2aa0f2a70241", "80 (tcp)"),
        ("53", "udp", "7d13438b-aed7-50a2-a3db-5efd18362b1b", "53 (udp)"),
    ],
)
def test_basic_ports(port_number, protocol, unique_id, port_str):
    port = Port(port_number=port_number, protocol=protocol)

    assert port.protocol == protocol
    assert port.port_number == int(port_number)

    assert port.unique_id == unique_id

    assert str(port) == port_str
