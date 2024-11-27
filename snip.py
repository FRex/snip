#!/usr/bin/env python3
"""A simple script to manage snippets of code using fzf and bat."""
import subprocess
import sys
import os


PIPE = subprocess.PIPE  # shortcut to make multiline Popen call a one liner


def find_printer_program():
    """Detect if bat is available and return "bat" or "cat" command to use."""

    try:
        args = ["bat", "--version"]
        res = subprocess.run(args, stdout=PIPE, check=False, stderr=PIPE)

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

    # NOTE: repr is to handle \\ on windows when given to bat
    # TODO: find a better way to do it in a crossplatform safe way?
    printer = find_printer_program()
    args = ["fzf", "--no-clear", f"--preview={printer} {repr(snipdir)}/{{}}", "--tac"]
    with subprocess.Popen(args, stdin=PIPE, stdout=PIPE, encoding="UTF-8") as proc:
        chosen = proc.communicate("\n".join(files))[0].strip()
        if proc.returncode != 0:
            print(f"return code is {proc.returncode} - doing nothing!", file=sys.stderr)
            sys.exit(proc.returncode)  # forward the return code

    # NOTE: even with spaces and backslashes, path with quotes around it works in cmd, ps and bash
    # NOTE: printing all diagnostics to stderr, only file goes to the stdout
    print(f'cd "{snipdir}"', file=sys.stderr)

    # dump entire file to stdout as binary to not convert newlines on windows
    # the flushing before and after is just in case (probably not needed)
    with open(os.path.join(snipdir, chosen), "rb") as file:
        sys.stdout.flush()
        sys.stdout.buffer.write(file.read())
        sys.stdout.flush()


if __name__ == "__main__":
    main()
