import argh
import csv
import json
import sys
import collections


def cast(obj):
    try:
        return float(obj)
    except:
        return obj


@argh.arg("-a", "--auto-cast", default=False)
def main(auto_cast=None):
    reader = csv.reader(sys.stdin)
    header = next(reader)

    for record in reader:
        obj = collections.OrderedDict((k, cast(v) if auto_cast else v)
                                      for k, v in zip(header, record))
        print json.dumps(obj)

    sys.stdout.flush()


def dispatch():
    argh.dispatch_command(main)


if __name__ == "__main__":
    dispatch()
