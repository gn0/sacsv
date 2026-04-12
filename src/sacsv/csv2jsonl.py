import click
import csv
import json
import sys
import collections


def cast(obj):
    try:
        return float(obj)
    except:
        return obj


def main(auto_cast=None):
    reader = csv.reader(sys.stdin)
    header = next(reader)

    for record in reader:
        obj = collections.OrderedDict((k, cast(v) if auto_cast else v)
                                      for k, v in zip(header, record))
        print(json.dumps(obj))

    sys.stdout.flush()


@click.command()
@click.help_option("-h", "--help", help="Show this message and exit")
@click.option(
    "--auto-cast",
    "-a",
    is_flag=True,
    default=False,
    help="Automatically cast values to float when possible",
)
def cli(auto_cast=None):
    """Convert CSV to JSON lines"""
    main(auto_cast)


if __name__ == "__main__":
    cli()
