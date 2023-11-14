import contextlib
import os
import tempfile
import typing
from enum import Enum
from pathlib import Path
from typing import Iterator

from .rename import rename


class Mode(str, Enum):
    TEXT = "TEXT"
    BYTES = "BYTES"


@contextlib.contextmanager
def file(
    file_name: str | Path, mode=Mode.TEXT, overwrite=False, tmp_dir=None
) -> Iterator[typing.IO]:
    # raise if tmp_dir doesn't exist ?
    fd, name = tempfile.mkstemp(dir=tmp_dir, suffix=".atomik")  # text mode here ?

    src = str(Path(name).absolute())
    dst = str(Path(file_name).absolute())

    f = os.fdopen(fd, "wt" if mode == Mode.TEXT else "wb")
    yield f
    f.close()

    rename(src, dst, overwrite=overwrite)


@contextlib.contextmanager
def folder(file_name: str | Path, tmp_dir=None) -> Path:
    file_name = file_name if isinstance(file_name, Path) else Path(file_name)
    name = tempfile.mkdtemp(dir=tmp_dir)
    yield Path(name)
    os.rename(name, file_name)
