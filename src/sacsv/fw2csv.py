import click
import re
import csv
import sys

from collections import OrderedDict


def parse_multiline_field_def(string):
    match = re.match(r"(?:(\d+):)?(\d+)-(\d+):(.+)", string)

    if match is None:
        raise ValueError("Field definition \"%s\" does not parse." % string)

    line_number = int(match.group(1) or "1")

    def extractor(lines):
        return (lines
                [line_number - 1]
                [slice(int(match.group(2)) - 1, int(match.group(3)))])

    return match.group(4), extractor


def get_multiline_extractors(field_defs):
    fields = OrderedDict()

    for field_def in field_defs:
        name, extractor = parse_multiline_field_def(field_def)
        fields[name] = extractor

    return fields


def iter_stacks_of(n, iterable):
    stack = tuple()

    for item in iterable:
        stack += (item,)

        if len(stack) == n:
            yield stack

            stack = tuple()

    if stack:
        yield stack


def main(lines_by_record=None, field=None):
    fields = get_multiline_extractors(field)

    writer = csv.writer(sys.stdout)
    writer.writerow(
        tuple(name for name in fields))
    writer.writerows(
        tuple(extractor(lines) for extractor in fields.values())
        for lines in iter_stacks_of(lines_by_record, sys.stdin))


@click.command()
@click.help_option("-h", "--help", help="Show this message and exit")
@click.option(
    "-l",
    "--lines-by-record",
    type=int,
    default=1,
    help="Number of lines per record in the fixed-width input",
)
@click.option(
    "-f",
    "--field",
    multiple=True,
    required=True,
    metavar="FIELD_SPEC",
    help="Field specification mapping fixed-width input to CSV column",
)
def cli(lines_by_record=None, field=None):
    """Extract CSV columns from fixed-width input

    Examples:

      One line per record in the fixed-width data:

    \b
        $ printf 'foo    1\\nbar    2\\n' | fw2csv -f 1-4:a -f 5-8:b
        a,b
        foo ,   1
        bar ,   2

      Two lines per record in the fixed-width data:

    \b
        $ printf 'foo    1\\nbar    2\\n' \\
          | fw2csv -l 2 -f 1-4:a -f 5-8:b -f 2:1-4:c -f 2:5-8:d
        a,b,c,d
        foo ,   1,bar ,   2
    """
    main(lines_by_record=lines_by_record, field=field)


if __name__ == "__main__":
    cli()
