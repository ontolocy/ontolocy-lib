# Open source cyber security graph framework

## Build cyber graphs with Python and Neo4j

Ontolocy is an open source framework for building cyber security graphs using Python, Pydantic, Pandas and a Neo4j graph database.

> **Ontolocy is currently in alpha, so things are likely to change and break.**

## Installation

```bash
pip install ontolocy
```

## Quick Start

### Setup Neo4j Connection Details

Put info in a local `.env` file.

```txt
# .env
NEO4J_URI=neo4j://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=Neo4jPassword

NEO4J_AUTH=neo4j/Neo4jPassword     # If running Neo4j with Docker
```

See [Neontology](https://github.com/ontolocy/neontology) for full details.

### Import MITRE ATT&CK Data into Neo4j

```bash
ontolocy parse mitre-attack
```

More on [MITRE ATT&CK to Neo4j](./ontolocy_parsers/MitreAttackParser.md).

### Examples

Notebooks on [github](https://github.com/ontolocy/ontolocy-lib/tree/main/examples)

Explore a [cyber graph](https://explore.ontolocy.com/) created with Ontolocy
