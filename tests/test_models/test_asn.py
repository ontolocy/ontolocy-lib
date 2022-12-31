from ontolocy.models.asn import ASN, ASNHasWhoIsRegisteredContact
from ontolocy.models.organisation import Organisation


def test_define_asn():

    my_asn = ASN(
        number="123",
        network_name="Example ASN",
        registry="arin",
        description="some asn",
        cidr="1.2.3.0/24",
        country_code="US",
    )

    assert my_asn.number == 123
    assert my_asn.network_name == "Example ASN"


def test_create_asn(use_graph):

    my_asn = ASN(
        number="123",
        network_name="Example ASN",
        registry="arin",
        description="some asn",
        cidr="1.2.3.0/24",
        country_code="US",
    )
    my_asn.create()

    cypher = """
    MATCH (n:ASN)
    WHERE n.number = 123
    RETURN n
    """

    result = use_graph.evaluate(cypher)

    assert result.has_label("ASN")

    assert result.get("number") == 123
    assert result.get("network_name") == "Example ASN"


def test_asn_registered_contact(use_graph):

    org = Organisation(name="GOOGLE LLC")
    org.merge()

    asn = ASN(
        number=15169,
        country_code="US",
        registry="arin",
        network_name="GOOGLE",
        description="GOOGLE - Google Inc., US",
        cidr="8.8.8.0/24",
    )
    asn.merge()

    rel = ASNHasWhoIsRegisteredContact(source=asn, target=org)
    rel.merge()

    cypher = """
    MATCH (asn:ASN)-[:ASN_HAS_REGISTERED_CONTACT]->(org:Organisation)
    WHERE asn.number = 15169
    RETURN COUNT(DISTINCT org)
    """

    result = use_graph.evaluate(cypher)

    assert result == 1
