import click
import sys
import csv

from sacsv import MultiValueOption, try_cast


def make_key_function(indices, auto_cast):
    if auto_cast:
        def key_function(record):
            return tuple(try_cast(record[i]) for i in indices)
    else:
        def key_function(record):
            return tuple(record[i] for i in indices)

    return key_function


def main(columns=None, delimiter=None, auto_cast=None):
    reader = csv.reader(sys.stdin, delimiter=delimiter)
    header = next(reader)

    if columns is None:
        indices = tuple(range(len(header)))
    else:
        indices = tuple(header.index(c) for c in columns)

    key = make_key_function(indices=indices, auto_cast=auto_cast)

    writer = csv.writer(sys.stdout)
    writer.writerow(header)

    for record in sorted(tuple(reader), key=key):
        writer.writerow(record)


@click.command()
@click.help_option("-h", "--help", help="Show this message and exit")
@click.option(
    "-c",
    "--columns",
    type=list[str],
    cls=MultiValueOption,
    metavar="COLUMN_NAME...",
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
@click.option(
    "--auto-cast",
    "-a",
    is_flag=True,
    default=False,
    help="Automatically cast arguments to int or float when possible",
)
def cli(columns=None, delimiter=None, auto_cast=None):
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
    main(columns=columns, delimiter=delimiter, auto_cast=auto_cast)


if __name__ == "__main__":
    cli()
