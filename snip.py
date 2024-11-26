#!/usr/bin/env python3
"""A simple script to manage snippets of code using fzf and bat."""
import subprocess
import sys
import os


def main():
    """Main function."""
    snipdir = os.path.join(os.path.dirname(__file__), "files")
    files = os.listdir(snipdir)
    args = ["fzf", f"--preview=bat {snipdir}/{{}}"]
    p = subprocess.Popen(
        args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        encoding="UTF-8",
    )

    out = p.communicate("\n".join(files))[0]

    if p.returncode != 0:
        print(f"return code is {p.returncode} - doing nothing", file=sys.stderr)
        return

    with open(os.path.join(snipdir, out.strip()), "rb") as fptr:
        sys.stdout.flush()
        sys.stdout.buffer.write(fptr.read())
        sys.stdout.flush()


if __name__ == "__main__":
    main()
