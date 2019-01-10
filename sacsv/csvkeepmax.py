import argh
import csv
import sys
import itertools as it


@argh.arg("-g", "--group-by", nargs="+", type=str, required=False)
@argh.arg("-c", "--column", type=str, required=True)
def main(group_by=None, column=None):
    reader = csv.reader(sys.stdin)
    header = next(reader)

    writer = csv.writer(sys.stdout)
    writer.writerow(header)

    if group_by is None:
        pick_group = lambda r: 1
    else:
        pick_group = lambda r: tuple(r[header.index(c)] for c in group_by)

    pick_column = lambda r: float(r[header.index(column)])

    for group, record_iter in it.groupby(
                                  sorted(reader, key=pick_group),
                                  pick_group):
        maximizers = tuple()
        maximum = None

        for record in record_iter:
            value = pick_column(record)

            if maximum is None:
                maximizers = (record,)
                maximum = value
            elif value >= maximum:
                if value > maximum:
                    maximizers = (record,)
                else:
                    maximizers += (record,)

                maximum = value

        if maximizers:
            writer.writerows(maximizers)


def dispatch():
    argh.dispatch_command(main)


if __name__ == "__main__":
    dispatch()
