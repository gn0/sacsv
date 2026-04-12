import click
import sys
import csv
import re


def main(columns=None, pattern=None, to=None):
    reader = csv.reader(sys.stdin)
    header = next(reader)

    indices = tuple(header.index(c) for c in columns)

    writer = csv.writer(sys.stdout)
    writer.writerow(header)

    for record in reader:
        writer.writerow(
            tuple(re.sub(pattern, to, value) if k in indices else value
                  for k, value in enumerate(record)))


@click.command()
@click.help_option("-h", "--help", help="Show this message and exit")
@click.option(
    "-c",
    "--columns",
    type=str,
    multiple=True,
    required=True,
    metavar="COLUMN_NAME",
    help="Names of one or more columns to perform substitution on",
)
@click.option(
    "-p",
    "--pattern",
    type=str,
    required=True,
    metavar="REGEX",
    help="Pattern to substitute",
)
@click.option(
    "-t",
    "--to",
    type=str,
    required=True,
    help="String to replace matches with",
)
def cli(columns=None, pattern=None, to=None):
    """Perform string substitution based on a regular expression

    Examples:

      Substitution in one column:

    \b
        $ printf 'a,b\\nfoo,bar\\n' | csvsed -c b -p '[fb]' -t 't'
        a,b
        foo,tar

      Substitution in two columns:

    \b
        $ printf 'a,b\\nfoo,bar\\n' | csvsed -c a -c b -p '[fb]' -t 't'
        a,b
        too,tar
    """
    main(columns=columns, pattern=pattern, to=to)


if __name__ == "__main__":
    cli()
