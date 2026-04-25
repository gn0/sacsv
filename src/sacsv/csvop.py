import click
import importlib
import csv
import sys
import operator as op

from sacsv import MultiValueOption, try_cast, make_pickers


def main(
    input_var,
    result_var,
    func_def,
    auto_cast=None,
    import_mod=None,
):
    for m in import_mod or tuple():
        globals()[m.split(".")[0]] = importlib.import_module(m.split(".")[0])
        importlib.import_module(m)

    f = eval(func_def)

    reader = csv.reader(sys.stdin)
    columns = next(reader)

    if result_var in columns:
        msg = f"Column {result_var} already exists in input"
        raise ValueError(msg)

    pickers = make_pickers(
        [columns.index(var) for var in input_var],
        auto_cast,
    )

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
    type=list[str],
    cls=MultiValueOption,
    metavar="MODULE_NAME...",
    help="Names of Python modules to import (e.g., 'math')",
)
@click.option(
    "-i",
    "--input-var",
    type=list[str],
    cls=MultiValueOption,
    required=True,
    metavar="COLUMN_NAME...",
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
    "--auto-cast",
    "-a",
    is_flag=True,
    default=False,
    help="Automatically cast arguments to int or float when possible",
)
@click.option(
    "-f",
    "--func-def",
    type=str,
    required=True,
    metavar="PYTHON_FUNC",
    help="Python function definition",
)
def cli(
    import_mod=None,
    input_var=None,
    result_var=None,
    auto_cast=None,
    func_def=None,
):
    """Apply a Python function to one or more columns

    Examples:

      Calculate word count:

    \b
        $ printf 'a\\nfoo bar\\nbaz\\n' \\
          | csvop -r b -i a -f 'lambda x: len(x.split())'
        a,b
        foo bar,2
        baz,1

      Sum two columns:

    \b
        $ printf 'a,b\\n1,2\\n3,4\\n' \\
          | csvop -r c -i a b -f 'lambda *x: sum(x)' -a
        a,b,c
        1,2,3
        3,4,7
    """
    main(
        input_var=input_var,
        result_var=result_var,
        func_def=func_def,
        auto_cast=auto_cast,
        import_mod=import_mod,
    )


if __name__ == "__main__":
    cli()
