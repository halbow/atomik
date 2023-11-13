import contextlib
import os
import tempfile
import typing
from pathlib import Path
from typing import Iterator



@contextlib.contextmanager
def file(file_name: str | Path) -> Iterator[typing.IO]:
    file_name = file_name if isinstance(file_name, Path) else Path(file_name)
    fd, name = tempfile.mkstemp()
    print(name)
    f = os.fdopen(fd, "wt")
    yield f
    f.close()
    os.rename(name, file_name)

@contextlib.contextmanager
def folder(file_name: str | Path) -> Path:
    file_name = file_name if isinstance(file_name, Path) else Path(file_name)
    name = tempfile.mkdtemp()
    yield Path(name)
    os.rename(name, file_name)


