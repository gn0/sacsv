import click
import importlib
import csv
import sys
import operator as op


def main(input_var, result_var, func_def, import_mod=None):
    for m in import_mod or tuple():
        globals()[m.split(".")[0]] = importlib.import_module(m.split(".")[0])
        importlib.import_module(m)

    f = eval(func_def)

    reader = csv.reader(sys.stdin)
    columns = next(reader)

    if result_var in columns:
        msg = f"Column {result_var} already exists in input"
        raise ValueError(msg)

    pickers = tuple(op.itemgetter(columns.index(var)) for var in input_var)

    writer = csv.writer(sys.stdout)
    writer.writerow(
        columns + [result_var])

    for i, record in enumerate(reader, 2):
        try:
            result = f(*tuple(pick_from(record) for pick_from in pickers))
        except Exception as e:
            msg = (
                f"Result variable {result_var}, {func_def}, line {i}: "
                f"{str(e)}"
            )
            raise type(e)(msg) from e

        writer.writerow(
            record + [result])


@click.command()
@click.help_option("-h", "--help", help="Show this message and exit")
@click.option(
    "-m",
    "--import-mod",
    type=str,
    multiple=True,
    metavar="MODULE_NAME",
    help="Python module to import before processing (e.g., 'math')",
)
@click.option(
    "-i",
    "--input-var",
    type=str,
    multiple=True,
    required=True,
    metavar="COLUMN_NAME",
    help="Names of columns to use as arguments to Python function",
)
@click.option(
    "-r",
    "--result-var",
    type=str,
    required=True,
    metavar="COLUMN_NAME",
    help="Name of new column to save function output to",
)
@click.option(
    "-f",
    "--func-def",
    # TODO Add -a/--auto-cast to convert values to float before feeding
    # them to the function in `func_def`.
    type=str,
    required=True,
    metavar="PYTHON_FUNC",
    help="Python function definition",
)
def cli(import_mod=None, input_var=None, result_var=None, func_def=None):
    """Apply a Python function to one or more columns"""
    main(
        input_var=input_var,
        result_var=result_var,
        func_def=func_def,
        import_mod=import_mod,
    )


if __name__ == "__main__":
    cli()
