import argh
import csv
import sys


def is_ascending(iterable):
    prev_value = None

    for value in iterable:
        if prev_value is not None and prev_value > value:
            return False

        prev_value = value

    return True


def is_descending(iterable):
    prev_value = None

    for value in iterable:
        if prev_value is not None and prev_value < value:
            return False

        prev_value = value

    return True


def main():
    reader = csv.reader(sys.stdin)
    header = next(reader)

    data = tuple(r for r in reader)

    for k, column in enumerate(header):
        if (is_ascending(r[k] for r in data)
            or is_descending(r[k] for r in data)):
            print(column)
            sys.exit(0)

        try:
            if is_ascending(float(r[k]) for r in data):
                print(column)
                sys.exit(0)
        except:
            pass

        try:
            if is_descending(float(r[k]) for r in data):
                print(column)
                sys.exit(0)
        except:
            pass


def dispatch():
    argh.dispatch_command(main)


if __name__ == "__main__":
    dispatch()
