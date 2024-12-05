#!/usr/bin/env python3
"""A simple script to manage snippets of code using fzf and bat."""
import subprocess
import sys
import os


def find_printer_program():
    """Detect if bat is available and return "bat" or "cat" command to use."""

    try:
        args = ["bat", "--version"]
        res = subprocess.run(
            args, stdout=subprocess.PIPE, check=False, stderr=subprocess.PIPE
        )

        # non-empty stderr or non-zero return code => default to cat
        if res.stderr or res.returncode != 0:
            return "cat"

        # bat's --version option prints bat and then a version number so check
        if res.stdout.startswith(b"bat"):
            return "bat --color=always"

    # bat not found in path at all so subprocess.run threw
    except FileNotFoundError:
        pass

    # default to cat
    return "cat"


def main():
    """Main function."""

    # TODO: make this snipdir come from env, config, etc.
    snipdir = os.path.join(os.path.dirname(__file__), "files")
    files = sorted(os.listdir(snipdir))  # sort files alphabetically

    # NOTE: even with spaces and backslashes, path with quotes around it works in cmd, ps and bash
    # NOTE: printing all diagnostics to stderr, only file goes to the stdout
    # NOTE: printing here so if fzf is cancelled with Ctrl-C this still shows up
    print(f'cd "{snipdir}"\n', file=sys.stderr)

    # NOTE: repr is to handle \\ on windows when given to bat
    # TODO: find a better way to do it in a crossplatform safe way?
    printer = find_printer_program()
    print(f"printer program is: {printer}\n", file=sys.stderr)
    args = ["fzf", "--no-clear", "--tac"]
    args.append(f"--preview={printer} {repr(snipdir)}/{{}}")

    result = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        encoding="UTF-8",
        input="\n".join(files),
        check=False,
    )

    # return code non-zero, try print a hint if its SIGINT aka signal 2 + 128 = 130
    if result.returncode != 0:
        note = " "
        if result.returncode == 130:
            note = " (SIGINT from Ctrl + C) "
        print(
            f"return code is {result.returncode}{note}- doing nothing!",
            file=sys.stderr,
        )
        sys.exit(result.returncode)  # forward the return code

    # by now we know we pickd a file, so grab that filename, minus newlines and spaces at ends
    chosen = result.stdout.strip()

    # dump entire file to stdout as binary to not convert newlines on windows
    # the flushing before and after is just in case (probably not needed?)
    print(f'dumping "{os.path.join(snipdir, chosen)}" to stdout\n', file=sys.stderr)
    with open(os.path.join(snipdir, chosen), "rb") as file:
        sys.stdout.flush()
        sys.stdout.buffer.write(file.read())
        sys.stdout.flush()


if __name__ == "__main__":
    main()
