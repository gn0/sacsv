import argh
import csv
import json
import sys
import collections


def main():
    reader = csv.reader(sys.stdin)
    header = next(reader)

    for record in reader:
        obj = collections.OrderedDict((k, v) for k, v in zip(header, record))
        print json.dumps(obj)

    sys.stdout.flush()


def dispatch():
    argh.dispatch_command(main)


if __name__ == "__main__":
    dispatch()
