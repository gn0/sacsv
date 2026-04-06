import argh
import importlib
import csv
import sys
import operator as op


@argh.arg("-m", "--import-mod", type=str, nargs="+", required=False)
@argh.arg("-i", "--input-var", type=str, nargs="+", required=True)
@argh.arg("-r", "--result-var", type=str, required=True)
@argh.arg("-f", "--func-def", type=str, required=True)
def main(import_mod=None, result_var=None, input_var=None, func_def=None):
    for m in import_mod or tuple():
        globals()[m.split(".")[0]] = importlib.import_module(m.split(".")[0])
        importlib.import_module(m)

    f = eval(func_def)

    reader = csv.reader(sys.stdin)
    columns = next(reader)
    pickers = tuple(op.itemgetter(columns.index(var)) for var in input_var)

    writer = csv.writer(sys.stdout)
    writer.writerow(
        columns + [result_var])

    for i, record in enumerate(reader, 2):
        try:
            result = f(*tuple(pick_from(record) for pick_from in pickers))
        except:
            import six

            exception, value, traceback = sys.exc_info()
            six.reraise(
                type(value),
                type(value)("Result variable %s, %s, line %d: %s"
                            % (result_var, func_def, i, str(value))),
                traceback)

        writer.writerow(
            record + [result])


def dispatch():
    argh.dispatch_command(main)


if __name__ == "__main__":
    dispatch()
