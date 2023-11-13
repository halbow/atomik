import contextlib
import os
import tempfile
import typing
from enum import Enum
from pathlib import Path
from typing import Iterator

class Mode(str, Enum):
    TEXT = "TEXT"
    BYTES = "BYTES"


@contextlib.contextmanager
def file(file_name: str | Path, mode=Mode.TEXT) -> Iterator[typing.IO]:
    file_name = file_name if isinstance(file_name, Path) else Path(file_name)
    fd, name = tempfile.mkstemp()
    f = os.fdopen(fd, "wt" if mode == Mode.TEXT else "wb")
    yield f
    f.close()
    os.rename(name, file_name)


@contextlib.contextmanager
def folder(file_name: str | Path) -> Path:
    file_name = file_name if isinstance(file_name, Path) else Path(file_name)
    name = tempfile.mkdtemp()
    yield Path(name)
    os.rename(name, file_name)


