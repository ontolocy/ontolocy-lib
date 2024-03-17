# Ontolocy

An open source cyber security graph ontology.

Use Python and Neo4j to explore cyber security data as a graph.

Currently in alpha/proof-of-concept stage - the ontology is likely to change (there may be breaking changes between minor releases).

> "All models are wrong, but some are useful" - George Box

Read the [docs](https://ontolocy.readthedocs.io/)

## Built with Ontolocy

* [Ontolocy Explore](https://explore.ontolocy.com/)

## Quick Start

### Install Ontolocy

```bash
pip install ontolocy
```

### Setup Neo4j Connection Details

Put info in a local `.env` file.

```txt
# .env
NEO4J_URI=neo4j://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password

NEO4J_AUTH=neo4j/your-password      # If running Neo4j with Docker
```

### Import MITRE ATT&CK Data into Neo4j

```bash
ontolocy parse mitre-attack
```
