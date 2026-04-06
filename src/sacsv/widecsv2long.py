import argh
import sys
import csv
import re
import operator as op


def drop_dups(iterable):
    seen = set()

    for item in iterable:
        if item not in seen:
            seen.add(item)

            yield item


@argh.arg("-v", "--var-re", type=str, nargs="+")
@argh.arg("-r", "--repeat-var-re", type=str, nargs="+")
@argh.arg("-i", "--index-name", type=str, required=True)
def main(var_re=None, repeat_var_re=None, index_name=None):
    # Compile patterns.
    #
    var_patterns = tuple(re.compile(p) for p in var_re or tuple())
    repeat_var_patterns = tuple(re.compile(p) for p in repeat_var_re)

    if any(p.groups < 2 for p in repeat_var_patterns):
        raise Exception("For every repeat variable pattern, must explicitly define two groups, one for the stub, and another for the repeat index.")
    elif any(p.groups > 2 for p in repeat_var_patterns):
        raise NotImplementedError("Nested repeat groups are not implemented yet.")

    # Read column names.
    #
    reader = csv.reader(sys.stdin)
    columns = next(reader)

    # Construct column names and column pickers for non-repeat
    # variables.
    #
    var_columns = tuple(column
                        for p in var_patterns or tuple()
                        for column in columns
                        if p.match(column))
    var_pickers = tuple(op.itemgetter(k)
                        for p in var_patterns or tuple()
                        for k, column in enumerate(columns)
                        if p.match(column))

    # Construct column names and column pickers for repeat va-
    # riables.
    #
    repeat_stubs = tuple(
                       drop_dups(
                           p.match(column).group(1)
                           for p in repeat_var_patterns
                           for column in columns
                           if p.match(column)))
    repeat_indices = set(p.match(column).group(2)
                         for p in repeat_var_patterns
                         for column in columns
                         if p.match(column))

    if all(re.match(r"^\d+$", x) for x in repeat_indices):
        repeat_indices = sorted(repeat_indices, key=lambda x: int(x))
    else:
        repeat_indices = sorted(repeat_indices)
#    repeat_var_pickers = (
#        tuple(
#            tuple(op.itemgetter(k)
#                  for p in repeat_var_patterns
#                  for k, column in enumerate(columns)
#                  if p.match(column) and p.match(column).group(2) == index)
#            for index in repeat_indices))

    repeat_var_pickers = []

    for index in repeat_indices:
        indexed_pickers = []

        for stub in repeat_stubs:
            found_indexed_column = False

            for p in repeat_var_patterns:
                for k, column in enumerate(columns):
                    if (not found_indexed_column
                        and p.match(column)
                        and p.match(column).group(1) == stub
                        and p.match(column).group(2) == index):
                        #print "Adding indexed picker for column '%s' (stub '%s', index %s)." % (column, stub, index)
                        indexed_pickers.append(
                            op.itemgetter(k))

                        found_indexed_column = True

            if not found_indexed_column:
                #print "Adding dummy indexed picker (stub '%s', index %s)." % (stub, index)
                indexed_pickers.append(
                    lambda r: "")

        repeat_var_pickers.append(
            indexed_pickers)

    # Write header.
    #
    writer = csv.writer(sys.stdout)
    writer.writerow(var_columns + (index_name,) + repeat_stubs)

    # Iterate through input, process it, and write it to output.
    #
    for record in reader:
        for index, indexed_var_pickers in zip(repeat_indices,
                                              repeat_var_pickers):
            var_values = tuple(pick(record) for pick in var_pickers)
            repeat_var_values = tuple(pick(record)
                                      for pick in indexed_var_pickers)

            if any(v != "" for v in repeat_var_values):
                writer.writerow(
                    var_values
                    + (index,)
                    + repeat_var_values)


def dispatch():
    argh.dispatch_command(main)


if __name__ == "__main__":
    dispatch()
