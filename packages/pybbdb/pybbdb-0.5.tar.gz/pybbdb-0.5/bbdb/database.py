"""
The BBDB database.
"""

import subprocess
from pathlib import Path
from typing import Optional

from .model import BBDB


def readdb(path: Optional[str] = None) -> BBDB:
    """Read a BBDB database.
    """

    return BBDB.fromfile(path or bbdb_file())


def bbdb_file() -> str:
    """Return the pathname of your BBDB file.

    This is the file referred to by the 'bbdb-file' variable in emacs.
    The most reliable way to get it is to ask emacs directly.
    """

    tag = "BBDB="
    cmd = "emacs --batch"
    cmd += " --eval '(load-file (expand-file-name \"~/.emacs\"))'"
    cmd += " --eval '(message \"%s%%s\" bbdb-file)' --kill" % tag

    text = subprocess.check_output(cmd, shell=True,
                                   stderr=subprocess.STDOUT)

    for line in text.decode('utf-8').split("\n"):
        if line.startswith(tag):
            path = line.replace(tag, "").strip()
            return str(Path(path).expanduser())

    raise RuntimeError("can't find BBDB file in emacs output")
