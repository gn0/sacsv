import math
from functools import partial
from typing import Callable
import click
import click.parser


# Based on Stephen Rauch's Stack Overflow answer:
#
#   https://stackoverflow.com/a/48394004
#
class MultiValueOption(click.Option):
    """`click.Option` variant that consumes multiple values.

    For example, `sacsv.csvsed.cli` declares `-c`/`--columns` to be a
    `MultiValueOption`, so `csvsed -c a b -p x -t y` replaces every
    occurrence of `x` with `y` in two columns, `a` and `b`.

    The implementation of this class is a hack.  It monkey patches
    `click.Option` by relying on parsing internals that are deprecated
    and will be removed in Click 9.0.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "nargs" in kwargs:
            msg = "MultiValueOption does not support 'nargs'"
            raise ValueError(msg)

        self._mvo_orig_process: Callable | None = None

    def add_to_parser(
        self,
        parser: click.parser._OptionParser,
        ctx: click.Context,
    ) -> None:
        super().add_to_parser(parser, ctx)

        def process_greedily(value, state):
            values = [value]

            while state.rargs and not state.rargs[0].startswith("-"):
                values.append(state.rargs.pop(0))

            assert self._mvo_orig_process is not None

            self._mvo_orig_process(values, state)

        # Override the `_Option.process` method that would handle values
        # for our option.
        #

        long_opt = parser._long_opt
        short_opt = parser._short_opt
        opt_parser: click.parser._Option | None = None

        for x in self.opts:
            if opt_parser := long_opt.get(x) or short_opt.get(x):
                break
        else:
            msg = f"Parser should know of option {'/'.join(self.opts)}"
            assert False, msg

        self._mvo_orig_process = opt_parser.process
        opt_parser.process = process_greedily # ty: ignore


def make_pickers(indices, auto_cast):
    result = []

    for index in indices:
        # NOTE Use `functools.partial` to prevent late binding of
        # `index` in the lambda expressions.
        #
        if auto_cast:
            picker = partial(
                lambda index, record: try_cast(record[index]),
                index,
            )
        else:
            picker = partial(lambda index, record: record[index], index)

        result.append(picker)

    return result


def try_cast(obj):
    """Convert to int if possible, or to float if possible."""
    if obj == "":
        return math.nan

    for convert in (int, float):
        try:
            return convert(obj)
        except:
            pass

    return obj
