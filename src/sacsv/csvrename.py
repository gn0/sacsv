import click
import csv
import sys


def main(column, new_column):
    reader = csv.reader(sys.stdin)
    header = next(reader)

    if new_column in header:
        raise ValueError("Column %s already exists." % new_column)

    new_header = (header[:header.index(column)]
                  + [new_column]
                  + header[header.index(column) + 1:])

    writer = csv.writer(sys.stdout)
    writer.writerow(new_header)
    writer.writerows(reader)


@click.command()
@click.help_option("-h", "--help", help="Show this message and exit")
@click.argument(
    "column",
    required=True,
    type=str,
    metavar="COLUMN_NAME",
)
@click.argument(
    "new_column",
    required=True,
    type=str,
    metavar="NEW_COLUMN_NAME",
)
def cli(column, new_column):
    """Rename a column"""
    main(column, new_column)


if __name__ == "__main__":
    cli()
