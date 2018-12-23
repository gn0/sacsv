import argh
import random
import csv
import sys


@argh.arg("-s", "--seed", type=int, required=True)
@argh.arg("-c", "--column-name", type=str, required=True)
def main(column_name=None, seed=None):
    random.seed(seed)

    reader = csv.reader(sys.stdin)
    header = next(reader)

    writer = csv.writer(sys.stdout)
    writer.writerow(
        header + [column_name])

    for record in reader:
        writer.writerow(
            record + [random.randint(1, 2**31)])


def dispatch():
    argh.dispatch_command(main)


if __name__ == "__main__":
    dispatch()
