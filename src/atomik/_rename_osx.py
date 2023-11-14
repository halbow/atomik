import ctypes
from .errors import AtomikError, FileAlreadyExistsError
from os import strerror, fsencode

libc = ctypes.CDLL("libc.dylib", use_errno=True)


RENAME = 0
RENAME_EXCHANGE = 1 << 1
RENAME_NOREPLACE = 1 << 2  # Not sure of the values ?

FILE_EXIST = 17


def _rename(src_path: str, dst_path: str, overwrite=False):
    relative_dir = -2
    code = libc.renameatx_np(
        relative_dir,
        fsencode(src_path),
        relative_dir,
        fsencode(dst_path),
        RENAME if overwrite else RENAME_NOREPLACE,
    )
    if code == 0:
        return
    else:
        errno = ctypes.get_errno()
        if errno == FILE_EXIST and strerror(errno) == "File exists":
            raise FileAlreadyExistsError
        raise AtomikError(f"Error during rename: {code}")
