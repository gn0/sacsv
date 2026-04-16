import click
import csv
import sys
import itertools as it

from sacsv import MultiValueOption


def main(group_by=None, column=None):
    reader = csv.reader(sys.stdin)
    header = next(reader)

    writer = csv.writer(sys.stdout)
    writer.writerow(header)

    if group_by is None:
        pick_group = lambda r: 1
    else:
        pick_group = lambda r: tuple(r[header.index(c)] for c in group_by)

    pick_column = lambda r: float(r[header.index(column)])

    for group, record_iter in it.groupby(
                                  sorted(reader, key=pick_group),
                                  pick_group):
        maximizers = tuple()
        maximum = None

        for record in record_iter:
            value = pick_column(record)

            if maximum is None:
                maximizers = (record,)
                maximum = value
            elif value >= maximum:
                if value > maximum:
                    maximizers = (record,)
                else:
                    maximizers += (record,)

                maximum = value

        if maximizers:
            writer.writerows(maximizers)


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
    "-c",
    "--column",
    type=str,
    required=True,
    metavar="COLUMN_NAME",
    help="Name of column by which to find maximum value",
)
def cli(group_by=None, column=None):
    """Keep the row that has the maximum value in a column"""
    main(group_by=group_by, column=column)


if __name__ == "__main__":
    cli()
