from ontolocy.models.dnsrecord import DNSRecord


def test_dnsrecord():
    record = DNSRecord(type="A", name="example.com", content="192.168.0.101")

    assert record.type == "A"
    assert record.unique_id is not None


def test_dnsrecord_same():
    record1 = DNSRecord(type="A", name="example.com", content="192.168.0.101")

    record2 = DNSRecord(type="A", name="example.com", content="192.168.0.101")

    assert record1.unique_id == record2.unique_id


def test_dnsrecord_different():
    record1 = DNSRecord(type="A", name="example.com", content="192.168.0.101")

    record2 = DNSRecord(type="A", name="example.com", content="192.168.0.102")

    assert record1.unique_id != record2.unique_id
