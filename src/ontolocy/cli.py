from pathlib import Path

import click

from ontolocy import init_ontolocy
from ontolocy.tools import MitreAttackParser

PARSERS = {
    "mitre-attack": {
        "parser_class": MitreAttackParser,
        "default_url": "https://github.com/mitre-attack/attack-stix-data/raw/master/enterprise-attack/enterprise-attack-14.1.json",
    }
}


@click.group()
def cli():
    pass


@cli.command()
@click.argument("parser_", type=click.Choice(PARSERS.keys()), nargs=1)
@click.option("--filepath", "-p", required=False)
@click.option("--url", "-u", required=False)
@click.option("--force", "-f", type=bool, default=False, required=False)
def parse(parser_, filepath, url, force):
    click.echo(f"parsing {parser_}...")

    parser = PARSERS[parser_]["parser_class"]()

    if filepath:
        path = Path(filepath)

        if path.exists is False:
            click.echo("Doesn't look like the file exists.")
            return

        parser.parse_file(str(path), populate=False)

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

        if new_nodes > 1000 or new_rels > 1000:
            msg += "\n\nThis might take a few minutes!"

        msg += "\n\nProceed to populate Neo4j?"

        if click.confirm(msg) is False:
            print("Goodbye")
            return

    print("populating the graph...")
    parser.populate()
    print("ingest complete")


if __name__ == "__main__":
    init_ontolocy()
    cli()
