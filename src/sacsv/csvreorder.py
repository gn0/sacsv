import argh
import sys
import csv


@argh.arg("-c", "--column-order", nargs="+", type=str, required=True)
def main(column_order=None):
    reader = csv.DictReader(sys.stdin)
    first_record = next(reader)

    columns = (
        tuple(column_order)
        + tuple(c for c in first_record
                  if c not in column_order))

    writer = csv.writer(sys.stdout)
    writer.writerow(columns)

    writer.writerow(
        tuple(first_record.get(c) for c in columns))
    for record in reader:
        writer.writerow(
            tuple(record.get(c) for c in columns))


def dispatch():
    argh.dispatch_command(main)


if __name__ == "__main__":
    dispatch()
