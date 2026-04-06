import sys
import csv
import multiprocessing as mp
import asyncio
import math
import io

import argh


async def run(argv, input):
    """Asynchronously executes a command.

    Arguments:
    argv -- list of the command and its arguments
    input -- string to be written to standard input
    """

    task = await asyncio.create_subprocess_exec(
        *argv,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    output, stderr = await task.communicate(input.encode())

    if stderr:
        print(stderr.decode(), file=sys.stderr)

    return output, task.returncode


def split_rows(num_batches, rows):
    "Splits rows into roughly equal-sized batches."

    num_rows = len(rows)
    num_rows_per_batch = math.ceil(num_rows / num_batches)

    for k in range(num_batches):
        yield rows[k * num_rows_per_batch : (k + 1) * num_rows_per_batch]


def format_as_csv(cells):
    string = io.StringIO()

    writer = csv.writer(string)
    writer.writerow(cells)

    return string.getvalue().strip("\r\n")


def append_csv_outputs(outputs):
    "Parses and appends a sequence of CSV formatted strings."

    readers = tuple(
        csv.reader(io.StringIO(output.decode()))
        for output in outputs)

    headers = tuple(next(reader) for reader in readers)
    distinct_headers = set(tuple(h) for h in headers)

    if len(distinct_headers) > 1:
        raise ValueError(
            "Command does not always return the same header: "
            + str(distinct_headers))

    appended_output = (headers[0],)
    appended_output += tuple(
        row
        for reader in readers
        for row in reader)

    return appended_output


async def command_dispatcher(jobs, command, args, header, rows):
    """Splits the input into batches, asynchronously executes
    the command for each batch, and appends their output."""

    tasks = tuple(
        run(
            (command,) + args,
            "%s\n%s" % (
                format_as_csv(header),
                "\n".join(format_as_csv(row) for row in task_rows)))
        for task_rows in split_rows(jobs, rows))

    results = await asyncio.gather(*tasks)

    output = append_csv_outputs(output for output, __ in results)
    exit_codes = tuple(exit_code for __, exit_code in results)

    return output, exit_codes


@argh.arg("-j", "--jobs", type=int, default=mp.cpu_count())
def main(command, *args, jobs=None):
    reader = csv.reader(sys.stdin)

    header = next(reader)
    rows = tuple(reader)

    output, exit_codes = asyncio.run(
        command_dispatcher(
            jobs, command, args, header, rows))

    writer = csv.writer(sys.stdout)
    writer.writerows(output)

    sys.exit(max(exit_codes))


def dispatch():
    argh.dispatch_command(main)


if __name__ == "__main__":
    dispatch()
