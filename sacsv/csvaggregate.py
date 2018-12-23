import argh
import importlib
import csv
import sys
import operator as op
import itertools as it


@argh.arg("-m", "--import-mod", type=str, nargs="+", required=False)
@argh.arg("-c", "--columns", type=str, nargs="+", required=True)
@argh.arg("-g", "--group-by", type=str, nargs="+", required=False)
@argh.arg("-f", "--func-def", type=str, required=True)
def main(import_mod=None, columns=None, group_by=None, func_def=None):
    for m in import_mod or tuple():
        globals()[m.split(".")[0]] = importlib.import_module(m.split(".")[0])
        importlib.import_module(m)

    f = eval(func_def)

    reader = csv.reader(sys.stdin)
    header = next(reader)
    pickers = tuple(op.itemgetter(header.index(c)) for c in columns)

    writer = csv.writer(sys.stdout)

    if group_by is None:
        group_key = lambda r: 1
        writer.writerow(columns)
    else:
        group_key = lambda r: tuple(r[header.index(c)] for c in group_by)
        writer.writerow(group_by + columns)

    for group_id, record_iter in it.groupby(
                                     sorted(
                                         reader,
                                         key=group_key),
                                     group_key):
        values = list(list() for k in xrange(len(columns)))

        for record in record_iter:
            for k in xrange(len(columns)):
                values[k].append(
                    pickers[k](record))

        if group_by is None:
            writer.writerow(
                tuple(f(values[k]) for k in xrange(len(columns))))
        else:
            writer.writerow(
                group_id
                + tuple(f(values[k]) for k in xrange(len(columns))))


def dispatch():
    argh.dispatch_command(main)


if __name__ == "__main__":
    dispatch()
