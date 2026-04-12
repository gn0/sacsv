import click
import random
import csv
import sys


def main(column_name=None, seed=None):
    random.seed(seed)

    reader = csv.reader(sys.stdin)
    header = next(reader)

    writer = csv.writer(sys.stdout)
    writer.writerow(
        header + [column_name])

    for record in reader:
        writer.writerow(
            record + [random.randint(1, 2**31)])


@click.command()
@click.help_option("-h", "--help", help="Show this message and exit")
@click.option(
    "-s",
    "--seed",
    type=int,
    required=True,
    help="Random seed for reproducibility",
)
@click.option(
    "-c",
    "--column-name",
    type=str,
    required=True,
    metavar="COLUMN_NAME",
    help="Name of the new column",
)
def cli(column_name=None, seed=None):
    """Add a new column that contains a random integer"""
    main(column_name=column_name, seed=seed)


if __name__ == "__main__":
    cli()
