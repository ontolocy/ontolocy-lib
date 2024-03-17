import json
from collections import defaultdict

import pandas as pd
import pytest
from ontolocy import IPAddressHasOpenPort, IPAddressNode, ListeningSocket

from ontolocy.tools.parsers.ontolocy_parser import OntolocyParser

practice_data = json.dumps(
    {
        "SOCKETS": [
            {"ip_address": "192.168.1.1", "port": 80, "protocol": "tcp"},
            {"ip_address": "192.168.1.2", "port": 22, "protocol": "tcp"},
        ],
    }
)

practice_data2 = json.dumps(
    {
        "SOCKETS": [
            {"ip_address": "192.168.1.3", "port": 443, "protocol": "tcp"},
            {"ip_address": "192.168.1.4", "port": 8080, "protocol": "tcp"},
        ],
    }
)


class PracticeIPParser(OntolocyParser):
    node_types = [IPAddressNode, ListeningSocket]
    rel_types = [IPAddressHasOpenPort]

    def _detect(self, input_data) -> bool:
        try:
            json_data = json.loads(input_data)

        except json.decoder.JSONDecodeError:
            return False

        if "SOCKETS" not in json_data:
            return False

        return True

    def _parse(self, input_data, private_namespace=None) -> tuple:
        data = json.loads(input_data)

        input_df = pd.DataFrame.from_records(data["SOCKETS"]).rename(
            columns={"port": "port_number"}
        )

        input_df["namespace"] = private_namespace

        #
        # Process Nodes
        #

        # IP Addresses

        ip_df = input_df.drop(columns=["port_number", "protocol"])

        node_oriented_dfs = {}

        node_oriented_dfs[IPAddressNode.__primarylabel__] = ip_df

        # Listening Sockets

        ls_df = input_df

        node_oriented_dfs[ListeningSocket.__primarylabel__] = ls_df

        #
        # Process Relationships
        #

        rel_type = IPAddressHasOpenPort.__relationshiptype__

        rel_input_dfs = defaultdict(dict)

        rel_input_dfs[rel_type]["src_df"] = ip_df.copy()

        rel_input_dfs[rel_type]["tgt_df"] = ls_df.copy()

        return node_oriented_dfs, rel_input_dfs


def test_instantiate():
    with pytest.raises(TypeError):
        OntolocyParser()


def test_detect():
    parser = PracticeIPParser()

    assert parser.detect(practice_data) is True


def test_detect_bad():
    parser = PracticeIPParser()

    assert parser.detect("Not even json") is False


def test_raise_bad():
    parser = PracticeIPParser()

    with pytest.raises(ValueError):
        parser.parse_data("Not even json")


def test_parse():
    parser = PracticeIPParser(private_namespace="TESTING")

    parser.parse_data(practice_data, populate=False)

    for df in parser.node_oriented_dfs.values():
        assert len(df) == 2

    assert parser.node_oriented_dfs["IPAddress"].to_dict(orient="records") == [
        {"ip_address": "192.168.1.1", "namespace": parser.private_namespace},
        {"ip_address": "192.168.1.2", "namespace": parser.private_namespace},
    ]

    assert len(parser.rel_input_dfs["IP_ADDRESS_HAS_OPEN_PORT"]["src_df"]) == 2


def test_parse_data():
    parser = PracticeIPParser(private_namespace="TEST NAMESPACE")

    parser.parse_data(practice_data, populate=False)

    for df in parser.node_oriented_dfs.values():
        assert len(df) == 2

    assert parser.node_oriented_dfs["IPAddress"].to_dict(orient="records") == [
        {"ip_address": "192.168.1.1", "namespace": parser.private_namespace},
        {"ip_address": "192.168.1.2", "namespace": parser.private_namespace},
    ]

    assert len(parser.rel_input_dfs["IP_ADDRESS_HAS_OPEN_PORT"]["src_df"]) == 2


def test_parse_file(tmp_path):
    tmp_file = tmp_path / "input_data.json"
    tmp_file.write_text(practice_data)

    parser = PracticeIPParser()
    parser.parse_file(file_path=str(tmp_file), populate=False)

    assert (
        parser.data_inputs[0]
        == '{"SOCKETS": [{"ip_address": "192.168.1.1", "port": 80, "protocol": "tcp"}, {"ip_address": "192.168.1.2", "port": 22, "protocol": "tcp"}]}'
    )


def test_parse_dir(tmp_path):
    tmp_file = tmp_path / "input_data_a.json"
    tmp_file.write_text(practice_data)
    tmp_file2 = tmp_path / "input_data_b.json"
    tmp_file2.write_text(practice_data2)

    parser = PracticeIPParser()
    parser.parse_directory(dir_path=str(tmp_path), populate=False)

    assert (
        '{"SOCKETS": [{"ip_address": "192.168.1.1", "port": 80, "protocol": "tcp"}, {"ip_address": "192.168.1.2", "port": 22, "protocol": "tcp"}]}'
        in parser.data_inputs
    )

    assert (
        '{"SOCKETS": [{"ip_address": "192.168.1.3", "port": 443, "protocol": "tcp"}, {"ip_address": "192.168.1.4", "port": 8080, "protocol": "tcp"}]}'
        in parser.data_inputs
    )


def test_merge_nodes(use_graph):
    parser = PracticeIPParser()
    parser.parse_data(practice_data, populate=False)

    parser._merge_nodes()

    cypher = """
    MATCH (ip:IPAddress)
    RETURN COUNT(DISTINCT ip)
    """

    result = use_graph.evaluate_query_single(cypher)

    assert result == 2


def test_merge_nodes_twice(use_graph):
    parser = PracticeIPParser()
    parser.parse_data(practice_data, populate=False)

    parser._merge_nodes()
    parser._merge_nodes()

    cypher = """
    MATCH (ip:IPAddress)
    RETURN COUNT(DISTINCT ip)
    """

    result = use_graph.evaluate_query_single(cypher)

    assert result == 2


def test_generate_rels(use_graph):
    parser = PracticeIPParser()
    parser.parse_data(practice_data, populate=False)

    parser._merge_nodes()

    cypher = """
    MATCH (ip:IPAddress)
    RETURN COUNT(DISTINCT ip)
    """

    result = use_graph.evaluate_query_single(cypher)

    assert result == 2

    parser._generate_relationships()

    assert len(parser.rel_oriented_dfs["IP_ADDRESS_HAS_OPEN_PORT"]) == 2


def test_populate(use_graph):
    parser = PracticeIPParser()

    parser.parse_data(practice_data, populate=False)

    parser.populate()

    cypher = """
    MATCH p = (ip:IPAddress)-[r:IP_ADDRESS_HAS_OPEN_PORT]-(ls:ListeningSocket)
    RETURN COUNT(DISTINCT p)
    """

    result = use_graph.evaluate_query_single(cypher)

    assert result == 2


def test_populate_existing(use_graph):
    namespace = "TESTING"

    ip1 = IPAddressNode(ip_address="192.168.1.1", namespace=namespace)

    ip1.merge()

    parser = PracticeIPParser(private_namespace=namespace)

    parser.parse_data(practice_data, populate=False)

    parser.populate()

    cypher = """
    MATCH p = (ip:IPAddress)-[r:IP_ADDRESS_HAS_OPEN_PORT]-(ls:ListeningSocket)
    RETURN COUNT(DISTINCT p)
    """

    result = use_graph.evaluate_query_single(cypher)

    assert result == 2


def test_parse_data_and_populate(use_graph):
    parser = PracticeIPParser()

    parser.parse_data(input_data=practice_data, populate=True)

    cypher = """
    MATCH p = (ip:IPAddress)-[r:IP_ADDRESS_HAS_OPEN_PORT]-(ls:ListeningSocket)
    RETURN COUNT(DISTINCT p)
    """

    result = use_graph.evaluate_query_single(cypher)

    assert result == 2


def test_parse_dir_and_populate(tmp_path, use_graph):
    tmp_file = tmp_path / "input_data_a.json"
    tmp_file.write_text(practice_data)
    tmp_file2 = tmp_path / "input_data_b.json"
    tmp_file2.write_text(practice_data2)

    parser = PracticeIPParser()
    parser.parse_directory(dir_path=str(tmp_path), populate=True)

    cypher = """
    MATCH p = (ip:IPAddress)-[r:IP_ADDRESS_HAS_OPEN_PORT]-(ls:ListeningSocket)
    RETURN COUNT(DISTINCT p)
    """

    result = use_graph.evaluate_query_single(cypher)

    assert result == 4
