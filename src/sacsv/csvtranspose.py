import csv
import sys


def main():
    data = tuple(csv.reader(sys.stdin))

    writer = csv.writer(sys.stdout)
    writer.writerows(
        map(list, zip(*data)))


def dispatch():
    main()


if __name__ == "__main__":
    dispatch()
