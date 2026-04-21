import click
import csv
import json
import sys
import collections

from sacsv import try_cast


def main(auto_cast=None):
    reader = csv.reader(sys.stdin)
    header = next(reader)

    for record in reader:
        obj = collections.OrderedDict(
            (k, try_cast(v) if auto_cast else v)
            for k, v in zip(header, record)
        )
        print(json.dumps(obj))

    sys.stdout.flush()


@click.command()
@click.help_option("-h", "--help", help="Show this message and exit")
@click.option(
    "--auto-cast",
    "-a",
    is_flag=True,
    default=False,
    help="Automatically cast values to int or float when possible",
)
def cli(auto_cast=None):
    """Convert CSV to JSON lines

    Examples:

      Treating all cells as strings:

    \b
        $ printf 'a,b\\nfoo,1\\nbar,2\\n' | csv2jsonl
        {"a": "foo", "b": "1"}
        {"a": "bar", "b": "2"}

      Treating numeric cells as floating-point numbers:

    \b
        $ printf 'a,b\\nfoo,1\\nbar,2\\n' | csv2jsonl -a
        {"a": "foo", "b": 1.0}
        {"a": "bar", "b": 2.0}
    """
    main(auto_cast)


if __name__ == "__main__":
    cli()
