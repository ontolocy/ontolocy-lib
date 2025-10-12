"""Taken from neontology conftest file"""

import logging
import os

import pytest
from click.testing import CliRunner
from dotenv import load_dotenv
from neontology import GraphConnection, init_neontology
from neontology.graphengines import Neo4jConfig

logger = logging.getLogger(__name__)


@pytest.fixture(
    scope="session",
    params=[
        pytest.param(
            {
                "graph_config_vars": {
                    "uri": "TEST_NEO4J_URI",
                    "username": "TEST_NEO4J_USERNAME",
                    "password": "TEST_NEO4J_PASSWORD",
                },
                "graph_engine": "NEO4J",
            },
            id="neo4j-engine",
        ),
    ],
)
def get_graph_config(request, tmp_path_factory) -> tuple:
    load_dotenv()

    graph_engines = {
        "NEO4J": Neo4jConfig,
    }

    graph_config_vars = request.param["graph_config_vars"]

    graph_config = {}

    # build config using environment variables
    for key, value in graph_config_vars.items():
        graph_config[key] = os.getenv(value)
        assert (
            graph_config[key] is not None
        ), f"Environment variable {value} is not set."

    graph_engine = request.param["graph_engine"]

    config = graph_engines[graph_engine](**graph_config)

    return config


@pytest.fixture(
    scope="session",
)
def graph_db(request, tmp_path_factory, get_graph_config):
    load_dotenv()

    init_neontology(get_graph_config)

    gc = GraphConnection()

    gc.change_engine(get_graph_config)

    # confirm we're starting with an empty database
    cypher = """
    MATCH (n)
    RETURN COUNT(n)
    """

    node_count = gc.evaluate_query_single(cypher)

    # most backends will return 0
    # Grand will return an empty list
    assert (
        not node_count
    ), f"Looks like there are {node_count} nodes in the database, it should be empty."

    yield gc


def pytest_collection_modifyitems(config, items):
    """Automatically mark tests which use the graph with the 'uses_graph' markers"""
    for item in items:
        if "use_graph" in item.fixturenames:
            item.add_marker("uses_graph")


@pytest.fixture(scope="function")
def use_graph(request, graph_db):
    """Fixture to use the graph database in tests."""
    yield graph_db

    # at the end of every individual test function, we want to empty the database

    cypher = """
    MATCH (n) DETACH DELETE n;
    """

    graph_db.evaluate_query_single(cypher)


@pytest.fixture
def cli_runner(get_graph_config):
    graph_engine_vars = {
        "Neo4jConfig": "NEO4J",
        "MemgraphConfig": "MEMGRAPH",
    }

    graph_engine = graph_engine_vars[get_graph_config.__class__.__name__]

    cli_env = {
        "NEONTOLOGY_ENGINE": graph_engine,
    }

    if graph_engine == "NEO4J":
        cli_env = {
            **cli_env,
            "NEO4J_URI": get_graph_config.uri,
            "NEO4J_USERNAME": get_graph_config.username,
            "NEO4J_PASSWORD": get_graph_config.password,
        }

    elif graph_engine == "MEMGRAPH":
        cli_env = {
            **cli_env,
            "MEMGRAPH_URI": get_graph_config.uri,
            "MEMGRAPH_USERNAME": get_graph_config.username,
            "MEMGRAPH_PASSWORD": get_graph_config.password,
        }

    runner = CliRunner(env=cli_env)

    return runner
