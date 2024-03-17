# MITRE ATTACK to Neo4j

## MitreAttackParser

Ingest MITRE ATT&CK® data into a Neo4j database so that you can explore it as part of a cyber security graph.

ATT&CK is a comprehensive knowledge base of cyber actor tactics and techniques developed and maintained by MITRE. The parser works with the Enterprise ATTACK STIX data that MITRE generate and store on github [here](https://github.com/mitre-attack/attack-stix-data/tree/master/enterprise-attack).

To connect to your Neo4j graph, Ontolocy expects the following environment variables. The easiest way to do this is to keep them in a `.env` file - just make sure you don't commit it to any repositories.

```bash
# .env
NEO4J_URI=neo4j://localhost:7687
NEO4J_USERNAME=neo4j            # neo4j is the default username
NEO4J_PASSWORD=MyNeo4jPassword  # replace this with your password!
```

## CLI Usage

By default, the parser will try to obtain the raw ATT&CK stix data from github for parsing and populating Neo4j.

Due to the volume of data (about 2000 nodes and 20,000 relationships) it can take a few minutes to populate the graph.

```bash
ontolocy parse mitre-attack
```

To ingest ATT&CK data from a file:

```bash
ontolocy parse mitre-attack -p /path/to/file
```

To ingest ATT&CK data from a specific remote URL:

```bash
ontolocy parse mitre-attack -u https://github.com/mitre-attack/attack-stix-data/raw/master/enterprise-attack/enterprise-attack.json
```

## Library Usage

If you're writing a Python script, or working in a Jupyter Notebook, you can import the MitreAttackParser class.

```python
from ontolocy import init_ontolocy
from ontolocy.tools import MitreAttackParser


# By default, Ontolocy expects environment variables to be set as above.
#   (e.g. in a .env file).

init_ontolocy()

# If preferred, you can provide Neo4j connection details explicitly:
#
#     init_ontolocy(
#       neo4j_uri="neo4j://localhost:7687",
#       neo4j_username="neo4j",
#       neo4j_password="MyNeo4jPassword"
#     )
#

parser = MitreAttackParser()

parser.parse_file(<file_path>)

parser.parse_url(<url>)

# Parse the data without populating Neo4j
parser.parse_file(<file_path>, populate=False)
```

## Nodes Created

Nodes with the following labels will be created in Neo4j from parsed data:

* [MitreAttackGroup](../ontology/MitreAttackGroup.md)
* [MitreAttackCampaign](../ontology/MitreAttackCampaign.md)
* [MitreAttackSoftware](../ontology/MitreAttackSoftware.md)
* [MitreAttackTactic](../ontology/MitreAttackTactic.md)
* [MitreAttackTechnique](../ontology/MitreAttackTechnique.md)
* [MitreAttackDataSource](../ontology/MitreAttackDataSource.md)
* [MitreAttackDataComponent](../ontology/MitreAttackDataComponent.md)
* [MitreAttackMitigation](../ontology/MitreAttackMitigation.md)

## Relationships

Neo4j relationships with the following relationship types will be created:

* MITRE_TACTIC_INCLUDES_TECHNIQUE
* MITRE_ATTACK_GROUP_USES_TECHNIQUE
* MITRE_ATTACK_GROUP_USES_SOFTWARE
* MITRE_SUBTECHNIQUE_OF
* MITRE_CAMPAIGN_USES_SOFTWARE
* MITRE_CAMPAIGN_ATTRIBUTED_TO_INTRUSION_SET
* MITRE_CAMPAIGN_USES_TECHNIQUE
* MITRE_SOFTWARE_USES_TECHNIQUE
* MITRE_ATTACK_MITIGATION_DEFENDS_AGAINST_TECHNIQUE
* MITRE_ATTACK_DATA_COMPONENT_DETECTS_TECHNIQUE
* MITRE_ATTACK_DATA_SOURCE_HAS_COMPONENT
