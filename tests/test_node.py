from typing import ClassVar

from ontolocy import OntolocyNode, DataOrigin


def test_define_node():
    class CyberPerson(OntolocyNode):
        __primaryproperty__: ClassVar[str] = "name"
        __primarylabel__: ClassVar[str] = "CyberPerson"

        name: str

    person = CyberPerson(name="Foo")

    assert person.name == "Foo"


def test_ingest_node(use_graph):
    class CyberPerson(OntolocyNode):
        __primaryproperty__: ClassVar[str] = "name"
        __primarylabel__: ClassVar[str] = "CyberPerson"

        name: str

    person = CyberPerson(name="Foo")

    data_origin = DataOrigin(name="Test Case")

    person.ingest(data_origin=data_origin)

    cypher = """
    MATCH (o:DataOrigin)-[:ORIGIN_GENERATED]->(cp:CyberPerson)
    WHERE o.name = 'Test Case' AND cp.name = 'Foo'
    RETURN COUNT(DISTINCT cp)
    """

    result = use_graph.evaluate_query_single(cypher)

    assert result == 1
