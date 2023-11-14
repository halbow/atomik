import ctypes
import os
from pathlib import Path

from .errors import AtomikError, FileAlreadyExistsError, InvalidCrossDeviceError
from os import strerror, fsencode

libc = ctypes.CDLL("libc.so.6", use_errno=True)


RENAME = 0
RENAME_EXCHANGE = 1 << 1
RENAME_NOREPLACE = 1 << 2  # Not sure of the values ?

FILE_EXIST = 17
INVALID_CROSS_DEVICE = 18
# flag_unavailable = errno.EINVAL

AT_FDCWD = -100


def _rename(src_path: str, dst_path: str, overwrite=False):
    print(os.stat(src_path).st_dev)
    print(os.stat("./tests/TEST_DATA/").st_dev)

    code = libc.renameat2(
        AT_FDCWD,
        fsencode(src_path),
        AT_FDCWD,
        fsencode(dst_path),
        RENAME if overwrite else RENAME_NOREPLACE,
    )
    if code == 0:
        return
    else:
        errno = ctypes.get_errno()
        if errno == FILE_EXIST:
            raise FileAlreadyExistsError(strerror(errno))
        if errno == INVALID_CROSS_DEVICE:
            src_dev = os.stat(src_path).st_dev
            dst_dev = os.stat(Path(dst_path).parent).st_dev
            raise InvalidCrossDeviceError(f"{strerror(errno)} '{src_path}' -> '{dst_path}' ({src_dev} != {dst_dev})")
        raise AtomikError(f"Error during rename: {strerror(errno)}({errno})")
