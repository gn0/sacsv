import click
import csv
import sys

from sacsv import MultiValueOption


def make_selector(keys, columns):
    def selector(record):
        return tuple(record[columns.index(key)] for key in keys)

    return selector


def main(join_table=None, keys=None):
    with open(join_table, "r") as f:
        reader = csv.reader(f)
        join_columns = next(reader)
        join_selector = make_selector(keys, join_columns)

        join_records = dict()

        for record in reader:
            key = join_selector(record)
            join_records.setdefault(key, tuple())
            join_records[key] += (record,)

    reader = csv.reader(sys.stdin)
    input_columns = next(reader)
    input_selector = make_selector(keys, input_columns)

    columns = (input_columns
               + [column for column in join_columns
                         if column not in keys])

    writer = csv.writer(sys.stdout)
    writer.writerow(columns)

    for record in reader:
        key = input_selector(record)

        if key not in join_records:
            writer.writerow(
                record
                + [None] * (len(columns) - len(input_columns)))
        else:
            for join_record in join_records.get(key):
                writer.writerow(
                    record
                    + [join_record[i] for i, column in enumerate(join_columns)
                                      if column not in keys])


@click.command()
@click.help_option("-h", "--help", help="Show this message and exit")
@click.option(
    "-j",
    "--join-table",
    type=click.Path(exists=True),
    required=True,
    metavar="PATH",
    help="Path to CSV file to join",
)
@click.option(
    "-k",
    "--keys",
    type=list[str],
    cls=MultiValueOption,
    required=True,
    metavar="COLUMN_NAME...",
    help="Names of one or more columns to join rows by",
)
def cli(join_table=None, keys=None):
    """Perform a LEFT JOIN between two CSV files"""
    main(join_table=join_table, keys=keys)


if __name__ == "__main__":
    cli()
