from pathlib import Path

import atomik


def test__atomik_file(file_name, data):
    path = Path(file_name)
    with atomik.file(path) as f:
        assert not path.exists()
        print(data, file=f, end="")

    assert path.exists()
    with open(path) as f:
        assert f.read() == data



def test__atomik_folder(folder):
    file_1 = "data_1.csv"
    file_2 = "data_2.csv"
    with atomik.folder(Path(folder)) as path:
        path_1 = Path(path, file_1)
        with open(path_1, 'w') as f:
            print("data_1", file=f, end="")
        path_2 = Path(path, file_2)
        with open(path_2, 'w') as f:
            print("data_2", file=f, end="")

        assert not Path(folder, file_1).exists()
        assert not Path(folder, file_2).exists()

    assert Path(folder, file_1).exists()
    assert Path(folder, file_2).exists()

    with open(Path(folder, file_1)) as f:
        assert f.read() == "data_1"
    with open(Path(folder, file_2)) as f:
        assert f.read() == "data_2"