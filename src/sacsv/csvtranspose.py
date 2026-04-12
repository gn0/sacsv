import csv
import sys

import click


def main():
    data = tuple(csv.reader(sys.stdin))

    writer = csv.writer(sys.stdout)
    writer.writerows(
        map(list, zip(*data)))


@click.command()
@click.help_option("-h", "--help", help="Show this message and exit")
def cli():
    """Transpose rows and columns

    Example:

    \b
      $ printf 'a,b\\n1,2\\n3,4\\n' | csvtranspose
      a,1,3
      b,2,4
    """
    main()


if __name__ == "__main__":
    cli()
