import argh
import csv
import sys


def get_fieldnames(fieldnames_iter):
    return sorted(
               set(f
                   for fieldnames in fieldnames_iter
                   for f in fieldnames))


assert (get_fieldnames(
            (("a", "b"), ("a", "b", "c")))
        == ["a", "b", "c"])


def make_get_fields(*fieldnames):
    def get_fields(record):
        return tuple(record.get(field) for field in fieldnames)

    return get_fields


assert make_get_fields("a", "b")(dict(a=1)) == (1, None)


@argh.arg("csv_filename", nargs="+")
def main(csv_filename):
    dict_readers = tuple(csv.DictReader(open(filename, "r"))
                         for filename in csv_filename)

    fieldnames = get_fieldnames(r.fieldnames for r in dict_readers)
    get_fields = make_get_fields(*fieldnames)

    writer = csv.writer(sys.stdout)

    writer.writerow(fieldnames)
    writer.writerows(
        get_fields(record)
        for dict_reader in dict_readers
        for record in dict_reader)

    sys.stdout.flush()


def dispatch():
    argh.dispatch_command(main)


if __name__ == "__main__":
    dispatch()
