import click
import sys
import csv
import itertools as it

from sacsv import MultiValueOption


def main(group_by=None, sort_by=None, column_name=None):
    reader = csv.reader(sys.stdin)
    header = next(reader)

    if group_by is None:
        group_key = lambda r: 1
    else:
        group_indices = tuple(header.index(c) for c in group_by)
        group_key = lambda r: tuple(r[i] for i in group_indices)

    if sort_by is None:
        sort_key = lambda r: 1
    else:
        sort_indices = tuple(header.index(c) for c in sort_by)
        sort_key = lambda r: tuple(r[i] for i in sort_indices)

    writer = csv.writer(sys.stdout)
    writer.writerow(
        [column_name] + header)

    for group_id, group_iter in it.groupby(
                                    sorted(reader, key=group_key),
                                    group_key):
        for k, record in enumerate(sorted(group_iter, key=sort_key), 1):
            writer.writerow(
                [k] + record)


@click.command()
@click.help_option("-h", "--help", help="Show this message and exit")
@click.option(
    "-g",
    "--group-by",
    type=list[str],
    cls=MultiValueOption,
    metavar="COLUMN_NAME...",
    help="Names of one or more columns to group rows by",
)
@click.option(
    "-s",
    "--sort-by",
    type=list[str],
    cls=MultiValueOption,
    metavar="COLUMN_NAME...",
    help="One or more column names to sort rows by in each group",
)
@click.option(
    "-c",
    "--column-name",
    type=str,
    required=True,
    metavar="COLUMN_NAME",
    help="Name of the new column",
)
def cli(group_by=None, sort_by=None, column_name=None):
    """Add a new column that contains a unique ID for each row

    Examples:

      Globally unique ID:

    \b
        $ printf 'a,b\\n1,4\\n2,3\\n2,4\\n1,3\\n' | csvadduniqueid -c id
        id,a,b
        1,1,4
        2,2,3
        3,2,4
        4,1,3

      ID that is unique within group:

    \b
        $ printf 'a,b\\n1,4\\n2,3\\n2,4\\n1,3\\n' | csvadduniqueid -c id -g a
        id,a,b
        1,1,4
        2,1,3
        1,2,3
        2,2,4

      ID that is increasing in column:

    \b
        $ printf 'a,b\\n1,4\\n2,3\\n2,4\\n1,3\\n' \\
          | csvadduniqueid -c id -g a -s b
        id,a,b
        1,1,3
        2,1,4
        1,2,3
        2,2,4
    """
    main(group_by=group_by, sort_by=sort_by, column_name=column_name)


if __name__ == "__main__":
    cli()
