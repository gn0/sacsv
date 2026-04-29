import sys
import csv
import multiprocessing as mp
import asyncio
import math
import io

import click


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


@click.command()
@click.help_option("-h", "--help", help="Show this message and exit")
@click.option(
    "-j",
    "--jobs",
    type=int,
    default=mp.cpu_count(),
    help="Number of jobs to launch in parallel",
)
@click.argument("command", nargs=-1, required=True)
def cli(command, jobs=None):
    """Feed CSV rows to command in parallel

    Example:

      Process CSV with two workers that add their own PID to the output:

    \b
        $ printf 'a\n1\n2\n3\n' \
          | csvparallel -j 2 -- \
            csvop -i a -r b -m os -f 'lambda x: os.getpid()'
        a,b
        1,2371254
        2,2371254
        3,2371256
    """
    main(command[0], *command[1:], jobs=jobs)


if __name__ == "__main__":
    cli()
