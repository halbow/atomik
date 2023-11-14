import platform

cur_os = platform.system()

if cur_os == "Linux":
    from atomik._rename_linux import _rename
elif cur_os == "Darwin":
    from atomik._rename_osx import _rename
else:
    raise ValueError("Unsupported Platform ")


def rename(src_path: str, dst_path: str, overwrite=False):
    _rename(src_path, dst_path, overwrite)
