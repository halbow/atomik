import contextlib
import os
import shutil
import tempfile
import typing
from enum import Enum
from pathlib import Path
from typing import Iterator

from .flags import Flag
from .rename import rename


class Mode(str, Enum):
    TEXT = "TEXT"
    BYTES = "BYTES"


@contextlib.contextmanager
def file(
    file_name: str | Path,
    mode: Mode = Mode.TEXT,
    overwrite: bool = False,
    tmp_dir: str | Path = None,
) -> Iterator[typing.IO]:
    # raise if filename ends with / ?
    # raise if tmp_dir doesn't exist ?
    fd, name = tempfile.mkstemp(dir=tmp_dir, suffix=".atomik")  # text mode here ?

    src = str(Path(name).absolute())
    dst = str(Path(file_name).absolute())

    f = os.fdopen(fd, "wt" if mode == Mode.TEXT else "wb")
    yield f
    f.close()

    flag = Flag.RENAME if overwrite else Flag.RENAME_NOREPLACE
    rename(src, dst, flag)


@contextlib.contextmanager
def folder(
    file_name: str | Path,
    overwrite: bool = False,
    tmp_dir: str | Path = None,
) -> Path:
    name = tempfile.mkdtemp(dir=tmp_dir, suffix=".atomik")

    src = str(Path(name).absolute())
    dst = str(Path(file_name).absolute())

    yield Path(name)

    if overwrite:
        rename(src, dst, Flag.RENAME_EXCHANGE)
        shutil.rmtree(src)
    else:
        rename(src, dst)
