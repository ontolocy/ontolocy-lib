import click
from neontology import init_neontology
from neontology.tools import import_json, import_md, import_yaml

from ontolocy.models.actortype import populate_actor_types
from ontolocy.models.country import populate_countries
from ontolocy.models.sector import populate_sectors
from ontolocy.tools import (
    CapecParser,
    CisaKevParser,
    CTIDAttackMappingsParser,
    CWEParser,
    MitreAttackParser,
    NistCSF1Parser,
    NistCSF2Parser,
    NistSP80053v4Parser,
    NistSP80053v5Parser,
    NVDCVEEnricher,
)

PARSERS = {
    "ctid-attack-sp80053-v5": {
        "parser_class": CTIDAttackMappingsParser,
        "default_url": (
            "https://raw.githubusercontent.com/"
            "center-for-threat-informed-defense/mappings-explorer/refs"
            "/heads/main/mappings/nist_800_53/attack-16.1/nist_800_53-rev5/enterprise/"
            "nist_800_53-rev5_attack-16.1-enterprise.json"
        ),
    },
    "ctid-attack-sp80053-v4": {
        "parser_class": CTIDAttackMappingsParser,
        "default_url": (
            "https://raw.githubusercontent.com/center-for-threat-informed-defense/"
            "mappings-explorer/refs/heads/main/mappings/nist_800_53/attack-14.1/nist_800_53-rev4/enterprise"
            "/nist_800_53-rev4_attack-14.1-enterprise.json"
        ),
    },
    "ctid-attack-mappings": {
        "parser_class": CTIDAttackMappingsParser,
    },
    "capec": {
        "parser_class": CapecParser,
        "default_url": "https://capec.mitre.org/data/xml/capec_latest.xml",
    },
    "cwe": {
        "parser_class": CWEParser,
        "default_url": "https://cwe.mitre.org/data/xml/cwec_latest.xml.zip",
    },
    "cisa-kev": {
        "parser_class": CisaKevParser,
        "default_url": "https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv",
    },
    "mitre-attack": {
        "parser_class": MitreAttackParser,
        "default_url": "https://github.com/mitre-attack/attack-stix-data/raw/refs/heads/master/enterprise-attack/enterprise-attack.json",
    },
    "mitre-attack-ics": {
        "parser_class": MitreAttackParser,
        "default_url": "https://github.com/mitre-attack/attack-stix-data/raw/refs/heads/master/ics-attack/ics-attack.json",
    },
    "mitre-attack-mobile": {
        "parser_class": MitreAttackParser,
        "default_url": "https://github.com/mitre-attack/attack-stix-data/raw/refs/heads/master/mobile-attack/mobile-attack.json",
    },
    "nist-csf-1": {
        "parser_class": NistCSF1Parser,
        "default_url": "https://www.nist.gov/document/2018-04-16frameworkv11core1xlsx",
    },
    "nist-csf-2": {
        "parser_class": NistCSF2Parser,
        "default_url": "https://csrc.nist.gov/extensions/nudp/services/json/csf/download?olirids=all",
    },
    "nist-sp80053-v4": {
        "parser_class": NistSP80053v4Parser,
        "default_url": "https://csrc.nist.gov/csrc/media/Projects/risk-management/800-53%20Downloads/800-53r4/800-53-rev4-controls.csv",
    },
    "nist-sp80053-v5": {
        "parser_class": NistSP80053v5Parser,
        "default_url": "https://csrc.nist.gov/CSRC/media/Publications/sp/800-53/rev-5/final/documents/sp800-53r5-control-catalog.xlsx",
    },
}

IP_ENRICHERS = {"shodan": None}
CVE_ENRICHERS = {"nvd": NVDCVEEnricher}


@click.group()
def cli():
    pass


@cli.command()
@click.argument("parser_", type=click.Choice(list(PARSERS.keys())), nargs=1)
@click.option("--filepath", "-p", type=click.Path(exists=True), required=False)
@click.option("--url", "-u", required=False)
@click.option("--force", "-f", type=bool, default=False, required=False)
def parse(parser_, filepath, url, force):
    """Parse data from supported cyber security datasets."""
    init_neontology()

    click.echo(f"parsing {parser_}...")

    parser = PARSERS[parser_]["parser_class"]()

    if filepath:
        parser.parse_file(str(filepath), populate=False)

    elif url:
        parser.parse_url(url, populate=False)

    elif PARSERS[parser_].get("default_url"):
        parser.parse_url(PARSERS[parser_]["default_url"], populate=False)

    else:
        click.echo("Needed a URL or a filepath to data to process.")
        return

    new_nodes = 0
    new_rels = 0

    for node_df in parser.node_oriented_dfs.values():
        new_nodes += len(node_df.index)

    for rel_entry in parser.rel_input_dfs.values():
        if "src_df" in rel_entry:
            new_rels += len(rel_entry["src_df"].index)

    if force is False:
        msg = f"\nAction will create up to {new_nodes} new nodes and {new_rels} new relationships."

        if new_nodes > 7000 or new_rels > 5000:
            msg += "\n\nThis might take a few minutes!"

        msg += "\n\nProceed to populate Neo4j?"

        if click.confirm(msg) is False:
            click.echo("Goodbye")
            return

    click.echo("populating the graph...")
    parser.populate()
    click.echo("ingest complete")


@click.group()
def enrich():
    """Enrich data in the graph with external data sources."""
    pass


def run_enrichment(enricher, seeds_str, refresh):
    enricher.enrich(seeds_str, refresh_days=refresh)

    seeds = seeds_str.split(",")

    click.echo(f"Enriching {', '.join(seeds)} with {enricher.__class__.__name__}...")

    enricher.enrich(seeds, refresh_days=refresh)


@enrich.command("ip")
@click.argument("enricher_", type=click.Choice(list(IP_ENRICHERS.keys())), nargs=1)
@click.argument("seeds_", type=str, nargs=1)
@click.option("--refresh", "-r", type=int, default=None, required=False)
def enrich_ip(enricher_, seeds_, refresh):
    init_neontology()

    if enricher_ == "shodan":
        try:
            from ontolocy.tools import ShodanIPEnricher

        except ImportError as e:
            raise ImportError(
                "Could not import Shodan - did you install Ontolocy with the"
                " ontolocy[all] or ontolocy[shodan] option? Try reinstalling,"
                " or pip installing shodan separately."
            ) from e

        enricher = ShodanIPEnricher()

    else:
        enricher = IP_ENRICHERS[enricher_]()

    run_enrichment(enricher, seeds_, refresh)


@enrich.command("cve")
@click.argument("enricher_", type=click.Choice(list(CVE_ENRICHERS.keys())), nargs=1)
@click.argument("seeds_", type=str, nargs=1)
@click.option("--refresh", "-r", type=int, default=None, required=False)
def enrich_cve(enricher_, seeds_, refresh):
    init_neontology()

    enricher = CVE_ENRICHERS[enricher_]()

    run_enrichment(enricher, seeds_, refresh)


@click.group()
def query():
    """Query an external source to populate the graph."""
    pass


@query.command()
@click.argument("query", type=str, nargs=-1)
def shodan(query):
    init_neontology()

    try:
        from ontolocy.tools import ShodanOntolocyClient

    except ImportError as e:
        raise ImportError(
            "Could not import Shodan - did you install Ontolocy with the"
            " ontolocy[all] or ontolocy[shodan] option? Try reinstalling,"
            " or pip installing shodan separately."
        ) from e

    client = ShodanOntolocyClient()

    query = " ".join(query)

    click.echo("Running query...")

    try:
        client.query(query)
        click.echo("Query complete.")

    except ValueError:
        click.echo("No results found.")


@cli.command()
@click.argument(
    "source", type=click.Choice(["all", "countries", "sectors", "actor-types"]), nargs=1
)
def populate(source):
    """Populate the graph with included static data."""
    init_neontology()

    click.echo(f"Populating {source}...")

    if source == "all":
        populate_countries()
        populate_sectors()
        populate_actor_types()

    elif source == "countries":
        populate_countries()

    elif source == "sectors":
        populate_sectors()

    elif source == "actor-types":
        populate_actor_types()


@cli.command("import")
@click.argument("dir_path")
@click.argument(
    "file_type",
    default="md",
    type=click.Choice(["md", "yml", "json"], case_sensitive=False),
)
def ingest(dir_path: str, file_type: str) -> None:
    """Import static data from a given directory."""

    init_neontology()

    click.echo(f"Importing data from {dir_path}")

    try:
        if file_type == "md":
            click.echo("Importing markdown files...")
            import_md(dir_path)

        elif file_type == "yml":
            import_yaml(dir_path)

        elif file_type == "json":
            import_json(dir_path)

        else:
            click.echo("Invalid file type specified. See help.")

    except KeyError:
        click.echo(
            "Import failed, are all content nodes defined and registered with the NeontologyManager."
        )


cli.add_command(enrich)
cli.add_command(query)

if __name__ == "__main__":
    cli()
