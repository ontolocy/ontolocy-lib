from ontolocy import Host


def test_host():
    host = Host(hostname="Windows1")

    assert str(host) == "Windows1"


def test_host_different_namespaces():
    host1 = Host(hostname="Windows1")
    host2 = Host(hostname="Windows1")

    assert host1.get_pp() != host2.get_pp()


def test_host_same_namespaces():
    host1 = Host(hostname="Windows1", namespace="TestCase")
    host2 = Host(hostname="Windows1", namespace="TestCase")

    assert host1.get_pp() == host2.get_pp()


def test_host_defined_unique_id():
    host1 = Host(hostname="Windows1", unique_id="windows-1")

    assert host1.get_pp() == "windows-1"
