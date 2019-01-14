import argh
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


assert (tuple(iter_stacks_of(1, "abcdef"))
        == (("a",), ("b",), ("c",), ("d",), ("e",), ("f",)))
assert (tuple(iter_stacks_of(3, "abcdef"))
        == (("a", "b", "c"), ("d", "e", "f")))
assert (tuple(iter_stacks_of(3, "abcdefg"))
        == (("a", "b", "c"), ("d", "e", "f"), ("g",)))


@argh.arg("--lines-by-record", "-l", type=int, required=False)
@argh.arg("--field", "-f", nargs="*", required=True)
def main(lines_by_record=1, field=None):
    fields = get_multiline_extractors(field)

    writer = csv.writer(sys.stdout)
    writer.writerow(
        tuple(name for name in fields))
    writer.writerows(
        tuple(extractor(lines) for extractor in fields.itervalues())
        for lines in iter_stacks_of(lines_by_record, sys.stdin))


def dispatch():
    argh.dispatch_command(main)


if __name__ == "__main__":
    dispatch()
