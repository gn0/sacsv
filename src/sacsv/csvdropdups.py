import argh
import csv
import sys
import itertools as it


def make_key(key_columns, columns):
    if len(key_columns) == 0:
        return lambda x: 1
    else:
        def key(item):
            return tuple(item[columns.index(c)] for c in key_columns)

        return key


@argh.arg("-k", "--key", type=str, nargs="+", required=True)
@argh.arg("-f", "--keep-first", type=str, nargs="*")
@argh.arg("-l", "--keep-last", type=str, nargs="*")
def main(key=None, keep_first=None, keep_last=None):
    if keep_first is None and keep_last is None:
        raise argh.CommandError(
                  "Must specify either --keep-first or --keep-last.")
    elif keep_first is not None and keep_last is not None:
        raise argh.CommandError(
                  "Must specify either --keep-first or --keep-last "
                  + "but not both.")

    reader = csv.reader(sys.stdin)
    columns = next(reader)

    primary_key = make_key(key, columns)

    if keep_first is not None:
        secondary_key = make_key(keep_first, columns)
    else:
        secondary_key = make_key(keep_last, columns)

    writer = csv.writer(sys.stdout)
    writer.writerow(columns)

    for item_key, item_iter in it.groupby(
                                   sorted(
                                       reader,
                                       key=primary_key),
                                   primary_key):
        items = sorted(item_iter, key=secondary_key)

        if keep_first is not None:
            writer.writerow(items[0])
        else:
            writer.writerow(items[-1])


def dispatch():
    argh.dispatch_command(main)


if __name__ == "__main__":
    dispatch()
