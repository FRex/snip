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
    with open(os.path.join(snipdir, out.strip()), "rb") as fptr:
        sys.stdout.flush()
        sys.stdout.buffer.write(fptr.read())
        sys.stdout.flush()


if __name__ == "__main__":
    main()
