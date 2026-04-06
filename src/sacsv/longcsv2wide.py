import argh
import sys
import csv
import itertools as it


def make_picker(index):
    def f(r):
        return r[index]

    return f


@argh.arg("-w", "--within", type=str, nargs="+", required=True)
@argh.arg("-i", "--index-vars", type=str, nargs="+", required=True)
@argh.arg("-v", "--vars", type=str, nargs="+", required=True)
def main(within=None, index_vars=None, vars=None):
    reader = csv.reader(sys.stdin)
    header = next(reader)

    pick_within = lambda r: tuple(r[header.index(v)] for v in within)
    pick_index = lambda r: tuple(r[header.index(v)] for v in index_vars)
    # Lesson for posterity: Python generator expressions don't
    # preserve the scope for anonymous functions within the
    # items.  So the following line of code produces a dictio-
    # nary where the keys are different but each value is the
    # same:
    #
    # pick_vars = dict((v, lambda r: r[header.index(v)]) for v in vars)
    #
    pick_vars = dict((v, make_picker(header.index(v))) for v in vars)
    pick_rest = lambda r: tuple(r[header.index(v)] for v in header
                                if v not in within
                                   and v not in index_vars
                                   and v not in vars)

    data = tuple(reader)

    rest_vars = pick_rest(header)

    index_values = sorted(set(pick_index(r) for r in data))
    long_vars = tuple((("_".join(["%s"] * (1 + len(index_vars))))
                       % ((var,) + v))
                      for var in vars
                      for v in index_values)

    writer = csv.writer(sys.stdout)
    writer.writerow(
        pick_within(header)
        + rest_vars
        + long_vars)

    for within_id, within_iter in it.groupby(
                                      sorted(data, key=pick_within),
                                      pick_within):
        within_data = tuple(within_iter)

        index_values1 = sorted(pick_index(r) for r in within_data)
        index_values2 = sorted(set(index_values1))
        if len(index_values1) != len(index_values2):
            raise ValueError(
                      "Index tuples not unique within %s."
                      % within_id)

        if not rest_vars:
            rest_values = tuple()
        else:
            rest_values = sorted(set(pick_rest(r) for r in within_data))
            if len(rest_values) > 1:
                raise ValueError(
                          "Remaining variables not unique within %s."
                          % within_id)

            rest_values = rest_values[0]

        r_by_index_value = dict((pick_index(r), r) for r in within_data)
        long_values = tuple(pick_vars[var](r_by_index_value[v])
                                if v in r_by_index_value
                                else None
                            for var in vars
                            for v in index_values)

        writer.writerow(
            within_id
            + rest_values
            + long_values)


def dispatch():
    argh.dispatch_command(main)


if __name__ == "__main__":
    dispatch()
