"""Common interface to run all of the scripts."""
import os.path as op

from mcot.utils.scripts import ScriptDirectory


def main():
    """Runs one of the scripts from the command line."""
    ScriptDirectory(op.split(__file__)[0])()


if __name__ == '__main__':
    main()