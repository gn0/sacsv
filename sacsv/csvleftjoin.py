import argh
import csv
import sys


def make_selector(keys, columns):
    def selector(record):
        return tuple(record[columns.index(key)] for key in keys)

    return selector


@argh.arg("--join-table", "-j", type=str, required=True)
@argh.arg("--keys", "-k", nargs="+", type=str, required=True)
def main(join_table=None, keys=None):
    with open(join_table, "r") as f:
        reader = csv.reader(f)
        join_columns = reader.next()
        join_selector = make_selector(keys, join_columns)

        join_records = dict()

        for record in reader:
            key = join_selector(record)
            join_records.setdefault(key, tuple())
            join_records[key] += (record,)

    reader = csv.reader(sys.stdin)
    input_columns = reader.next()
    input_selector = make_selector(keys, input_columns)

    columns = (input_columns
               + [column for column in join_columns
                         if column not in keys])

    writer = csv.writer(sys.stdout)
    writer.writerow(columns)

    for record in reader:
        key = input_selector(record)

        if key not in join_records:
            writer.writerow(
                record
                + [None] * (len(columns) - len(input_columns)))
        else:
            for join_record in join_records.get(key):
                writer.writerow(
                    record
                    + [join_record[i] for i, column in enumerate(join_columns)
                                      if column not in keys])


def dispatch():
    argh.dispatch_command(main)


if __name__ == "__main__":
    dispatch()
