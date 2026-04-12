import click
import sys
import csv


def main(columns=None, delimiter=None):
    reader = csv.reader(sys.stdin, delimiter=delimiter)
    header = next(reader)

    if columns is None:
        key = lambda r: r
    else:
        indices = tuple(header.index(c) for c in columns)
        key = lambda r: tuple(r[index] for index in indices)

    writer = csv.writer(sys.stdout)
    writer.writerow(header)

    for record in sorted(tuple(reader), key=key):
        writer.writerow(record)


@click.command()
@click.help_option("-h", "--help", help="Show this message and exit")
@click.option(
    "-c",
    "--columns",
    type=str,
    multiple=True,
    metavar="COLUMN_NAME",
    help="Names of one or more columns to sort rows by",
)
@click.option(
    "-d",
    "--delimiter",
    type=str,
    default=",",
    metavar="CHAR",
    help="Delimiter (e.g., `,` for comma-separated values)",
)
def cli(columns=None, delimiter=None):
    """Sort rows by one or more columns

    Examples:

    \b
      $ printf 'a,b\\n3,2\\n1,4\\n' | csvsort
      a,b
      1,4
      3,2

    \b
      $ printf 'a,b\\n3,2\\n1,4\\n' | csvsort -c b
      a,b
      3,2
      1,4
    """
    main(columns=columns, delimiter=delimiter)


if __name__ == "__main__":
    cli()
