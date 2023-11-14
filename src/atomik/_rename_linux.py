import ctypes
import os
from pathlib import Path

from .errors import AtomikError, FileAlreadyExistsError, InvalidCrossDeviceError
from os import strerror, fsencode

libc = ctypes.CDLL("libc.so.6", use_errno=True)


RENAME = 0  # Equivalent to rename # https://man7.org/linux/man-pages/man2/rename.2.html
RENAME_NOREPLACE = 1  # Value found here https://github.com/torvalds/linux/blob/9bacdd8996c77c42ca004440be610692275ff9d0/include/uapi/linux/fs.h#L50

FILE_EXIST = 17
INVALID_CROSS_DEVICE = 18
# flag_unavailable = errno.EINVAL

AT_FDCWD = -100


def _rename(src_path: str, dst_path: str, overwrite=False):
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
            raise InvalidCrossDeviceError(
                f"{strerror(errno)} '{src_path}' -> '{dst_path}' ({src_dev} != {dst_dev})"
            )
        raise AtomikError(f"Error during rename: {strerror(errno)}({errno})")
