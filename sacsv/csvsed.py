import argh
import sys
import csv
import re


@argh.arg("-c", "--columns", type=str, nargs="+", required=True)
@argh.arg("-p", "--pattern", type=str, required=True)
@argh.arg("-t", "--to", type=str, required=True)
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


def dispatch():
    argh.dispatch_command(main)


if __name__ == "__main__":
    dispatch()
