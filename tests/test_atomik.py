from pathlib import Path

import pytest

import atomik
from atomik.errors import FileAlreadyExistsError


def test__atomik_file_1(file_name, data):
    path = Path(file_name)
    with atomik.file(path, tmp_dir="./tests/TEST_DATA/.tmp") as f:
        assert not path.exists()
        f.write(data)

    assert path.exists()
    with open(path) as f:
        assert f.read() == data


def test__atomik_folder(folder):
    file_1 = "data_1.csv"
    file_2 = "data_2.csv"
    with atomik.folder(Path(folder), tmp_dir="./tests/TEST_DATA/.tmp") as path:
        path_1 = Path(path, file_1)
        with open(path_1, "w") as f:
            f.write("data_1")
        path_2 = Path(path, file_2)
        with open(path_2, "w") as f:
            f.write("data_2")

        assert not Path(folder, file_1).exists()
        assert not Path(folder, file_2).exists()

    assert Path(folder, file_1).exists()
    assert Path(folder, file_2).exists()

    with open(Path(folder, file_1)) as f:
        assert f.read() == "data_1"
    with open(Path(folder, file_2)) as f:
        assert f.read() == "data_2"


def test_atomik_file_bytes(file_name, data):
    data = str.encode(data)
    path = Path(file_name)
    with atomik.file(path, mode=atomik.Mode.BYTES, tmp_dir="./tests/TEST_DATA/.tmp") as f:
        assert not path.exists()
        f.write(data)

    assert path.exists()
    with open(path, "rb") as f:
        assert f.read() == data


def test__atomik_file__file_present__raise(file_name, data):
    path = Path(file_name)
    path.touch()
    with pytest.raises(FileAlreadyExistsError):
        with atomik.file(path, tmp_dir="./tests/TEST_DATA/.tmp") as f:
            f.write(data)


def test__atomik_file__file_overwrite(file_name, data):
    path = Path(file_name)
    path.touch()
    with atomik.file(path, overwrite=True, tmp_dir="./tests/TEST_DATA/.tmp") as f:
        f.write(data)
    with open(path) as f:
        assert f.read() == data
