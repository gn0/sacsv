import argh
import sys
import csv
import itertools as it


@argh.arg("-g", "--group-by", type=str, nargs="+")
@argh.arg("-s", "--sort-by", type=str, nargs="+")
@argh.arg("-c", "--column-name", type=str, required=True)
def main(group_by=None, sort_by=None, column_name=None):
    reader = csv.reader(sys.stdin)
    header = next(reader)

    if group_by is None:
        group_key = lambda r: 1
    else:
        group_indices = tuple(header.index(c) for c in group_by)
        group_key = lambda r: tuple(r[i] for i in group_indices)

    if sort_by is None:
        sort_key = lambda r: 1
    else:
        sort_indices = tuple(header.index(c) for c in sort_by)
        sort_key = lambda r: tuple(r[i] for i in sort_indices)

    writer = csv.writer(sys.stdout)
    writer.writerow(
        [column_name] + header)

    for group_id, group_iter in it.groupby(
                                    sorted(reader, key=group_key),
                                    group_key):
        for k, record in enumerate(sorted(group_iter, key=sort_key), 1):
            writer.writerow(
                [k] + record)


def dispatch():
    argh.dispatch_command(main)


if __name__ == "__main__":
    dispatch()
