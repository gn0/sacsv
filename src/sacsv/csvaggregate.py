import click
import importlib
import csv
import sys
import operator as op
import itertools as it

from sacsv import MultiValueOption, make_pickers, try_cast


def main(
    import_mod=None,
    columns=None,
    group_by=None,
    func_def=None,
    auto_cast=None,
):
    for m in import_mod or tuple():
        globals()[m.split(".")[0]] = importlib.import_module(m.split(".")[0])
        importlib.import_module(m)

    f = eval(func_def)

    reader = csv.reader(sys.stdin)
    header = next(reader)
    pickers = make_pickers(
        [header.index(c) for c in columns],
        auto_cast,
    )

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
        values = list(list() for k in range(len(columns)))

        for record in record_iter:
            for k in range(len(columns)):
                values[k].append(
                    pickers[k](record))

        if group_by is None:
            writer.writerow(
                tuple(f(values[k]) for k in range(len(columns))))
        else:
            writer.writerow(
                group_id
                + tuple(f(values[k]) for k in range(len(columns))))


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
    "-c",
    "--columns",
    type=list[str],
    cls=MultiValueOption,
    required=True,
    metavar="COLUMN_NAME...",
    help="Names of columns to aggregate",
)
@click.option(
    "-g",
    "--group-by",
    type=list[str],
    cls=MultiValueOption,
    metavar="COLUMN_NAME...",
    help="Names of one or more columns to group rows by",
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
    columns=None,
    group_by=None,
    auto_cast=None,
    func_def=None,
):
    """Apply a Python function to aggregate groups of rows

    Examples:

      Calculate the arithmetic mean:

    \b
        $ printf 'a,b\\n1,1\\n1,2\\n2,2\\n2,1\\n' \\
          | csvaggregate -c b -f 'lambda x: sum(map(int, x)) / len(x)'
        b
        1.5

      Concatenate values for each group:

    \b
        $ printf 'a,b\\n1,1\\n1,2\\n2,2\\n2,1\\n' \\
          | csvaggregate -g a -c b -f 'lambda x: ":".join(x)'
        a,b
        1,1:2
        2,2:1
    """
    main(
        import_mod=import_mod,
        columns=columns,
        group_by=group_by,
        func_def=func_def,
        auto_cast=auto_cast,
    )


if __name__ == "__main__":
    main()
