import click
import csv
import sys


def get_fieldnames(fieldnames_iter):
    return sorted(
               set(f
                   for fieldnames in fieldnames_iter
                   for f in fieldnames))


def make_get_fields(*fieldnames):
    def get_fields(record):
        return tuple(record.get(field) for field in fieldnames)

    return get_fields


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


@click.command()
@click.help_option("-h", "--help", help="Show this message and exit")
@click.argument(
    "csv_filename",
    nargs=-1,
    required=True,
    type=click.Path(exists=True),
    metavar="PATH...",
)
def cli(csv_filename):
    """Append several CSV files, taking the union of their columns"""
    main(csv_filename)


if __name__ == "__main__":
    cli()
