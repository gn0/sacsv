import click
import csv
import sys
import itertools as it


def make_key(key_columns, columns):
    if len(key_columns) == 0:
        return lambda x: 1
    else:
        def key(item):
            return tuple(item[columns.index(c)] for c in key_columns)

        return key


def main(key=None, keep_first=None, keep_last=None):
    if keep_first is None and keep_last is None:
        click.echo(
            "error: Must specify either --keep-first or --keep-last.",
            err=True,
        )
        sys.exit(1)
    elif keep_first is not None and keep_last is not None:
        click.echo(
            "error: Must specify either --keep-first or --keep-last "
            "but not both.",
            err=True,
        )
        sys.exit(1)

    reader = csv.reader(sys.stdin)
    columns = next(reader)

    primary_key = make_key(key, columns)

    if keep_first is not None:
        secondary_key = make_key(keep_first, columns)
    else:
        secondary_key = make_key(keep_last, columns)

    writer = csv.writer(sys.stdout)
    writer.writerow(columns)

    for item_key, item_iter in it.groupby(
                                   sorted(
                                       reader,
                                       key=primary_key),
                                   primary_key):
        items = sorted(item_iter, key=secondary_key)

        if keep_first is not None:
            writer.writerow(items[0])
        else:
            writer.writerow(items[-1])


@click.command()
@click.help_option("-h", "--help", help="Show this message and exit")
@click.option(
    "-k",
    "--key",
    type=str,
    multiple=True,
    required=True,
    metavar="COLUMN_NAME",
    help="Names of one or more columns to define duplicates by",
)
@click.option(
    "-f",
    "--keep-first",
    type=str,
    multiple=True,
    metavar="COLUMN_NAME",
    help=(
        "Keep the first instance after sorting duplicates by these "
        "columns"
    ),
)
@click.option(
    "-l",
    "--keep-last",
    type=str,
    multiple=True,
    metavar="COLUMN_NAME",
    help=(
        "Keep the last instance after sorting duplicates by these "
        "columns"
    ),
)
def cli(key=None, keep_first=None, keep_last=None):
    """Drop duplicate rows"""
    main(key=key, keep_first=keep_first, keep_last=keep_last)


if __name__ == "__main__":
    cli()
