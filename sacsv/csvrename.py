import argh
import csv
import sys


def main(column, new_column):
    reader = csv.reader(sys.stdin)
    header = next(reader)

    if new_column in header:
        raise ValueError("Column %s already exists." % new_column)

    new_header = (header[:header.index(column)]
                  + [new_column]
                  + header[header.index(column) + 1:])

    writer = csv.writer(sys.stdout)
    writer.writerow(new_header)
    writer.writerows(reader)


def dispatch():
    argh.dispatch_command(main)


if __name__ == "__main__":
    dispatch()
