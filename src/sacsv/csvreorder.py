import click
import sys
import csv

from sacsv import MultiValueOption


def main(column_order=None):
    reader = csv.DictReader(sys.stdin)
    first_record = next(reader)

    columns = (
        tuple(column_order)
        + tuple(c for c in first_record
                  if c not in column_order))

    writer = csv.writer(sys.stdout)
    writer.writerow(columns)

    writer.writerow(
        tuple(first_record.get(c) for c in columns))
    for record in reader:
        writer.writerow(
            tuple(record.get(c) for c in columns))


@click.command()
@click.help_option("-h", "--help", help="Show this message and exit")
@click.option(
    "-c",
    "--column-order",
    type=list[str],
    cls=MultiValueOption,
    required=True,
    metavar="COLUMN_NAME...",
    help="Names of one or more columns in the order to print them",
)
def cli(column_order=None):
    """Change the order of CSV columns"""
    main(column_order)


if __name__ == "__main__":
    cli()
