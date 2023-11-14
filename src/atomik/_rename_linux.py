import ctypes
import errno
from atomik.errors import AtomikError, FileAlreadyExistsError
from os import strerror, fsencode

libc = ctypes.CDLL(None, use_errno=True)


RENAME = 0
RENAME_EXCHANGE = 1 << 1
RENAME_NOREPLACE = 1 << 2  # Not sure of the values ?

FILE_EXIST = 17
flag_unavailable = errno.EINVAL


def _rename(src_path: str, dst_path: str, overwrite=False):
    relative_dir = -100
    code = libc.renameat2(
        relative_dir,
        src_path,
        relative_dir,
        dst_path,
        RENAME if overwrite else RENAME_NOREPLACE,
    )
    if code == 0:
        return
    else:
        raise AtomikError(f"Error during rename: {code}")
