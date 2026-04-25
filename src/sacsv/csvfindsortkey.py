import click
import csv
import math
import sys

from sacsv import try_cast


def is_ascending(iterable):
    prev_value = None

    for value in iterable:
        if isinstance(value, float) and math.isnan(value):
            continue

        if prev_value is not None and prev_value > value:
            return False

        prev_value = value

    return True


def is_descending(iterable):
    prev_value = None

    for value in iterable:
        if isinstance(value, float) and math.isnan(value):
            continue

        if prev_value is not None and prev_value < value:
            return False

        prev_value = value

    return True


def main():
    reader = csv.reader(sys.stdin)
    header = next(reader)

    data = tuple(r for r in reader)

    for k, column in enumerate(header):
        for convert in (try_cast, lambda x: x):
            try:
                if (is_ascending(convert(r[k]) for r in data)
                    or is_descending(convert(r[k]) for r in data)):
                    print(column)
                    sys.exit(0)
            except TypeError:
                pass


@click.command()
@click.help_option("-h", "--help", help="Show this message and exit")
def cli():
    """Find the column by which the input is sorted

    Examples:

      Input is sorted in ascending order:

    \b
        $ printf 'a,b\\n92,1\\n59,2\\n67,3\\n' | csvfindsortkey
        b

      Input is sorted in descending order:

    \b
        $ printf 'a,b\\n92,3\\n59,2\\n67,1\\n' | csvfindsortkey
        b

      Input has no apparent sort key:

    \b
        $ printf 'a,b\\n92,1\\n59,3\\n67,2\\n' | csvfindsortkey
        [No output.]
    """
    main()


if __name__ == "__main__":
    cli()
