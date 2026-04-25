import click
import csv
import math
import sys
import itertools as it

from sacsv import MultiValueOption


def cast_to_numeric(obj):
    """Convert to int or float if possible, or throw ValueError."""
    if obj == "":
        return math.nan

    try:
        return int(obj)
    except ValueError:
        pass

    return float(obj)


def main(column, group_by=None):
    reader = csv.reader(sys.stdin)
    header = next(reader)

    writer = csv.writer(sys.stdout)
    writer.writerow(header)

    if group_by is None:
        def pick_group(record):
            return 1
    else:
        def pick_group(record):
            return tuple(record[header.index(c)] for c in group_by)

    def pick_column(record):
        return cast_to_numeric(record[header.index(column)])

    for group, record_iter in it.groupby(
                                  sorted(reader, key=pick_group),
                                  pick_group):
        maximizers = tuple()
        maximum = None

        for record in record_iter:
            value = pick_column(record)

            if math.isnan(value):
                continue

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
    """Keep the row that has the maximum value in a column

    Examples:

      Keeping rows that contain the global maximum:

    \b
        $ printf 'a,b\\n1,1\\n1,2\\n2,2\\n3,1\\n' | csvkeepmax -c b
        a,b
        1,2
        2,2

      Keeping rows that contain their group's maximum:

    \b
        $ printf 'a,b\\n1,1\\n1,2\\n2,2\\n3,1\\n' | csvkeepmax -c b -g a
        a,b
        1,2
        2,2
        3,1
    """
    main(group_by=group_by, column=column)


if __name__ == "__main__":
    cli()
