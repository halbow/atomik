from pathlib import Path

from atomik import atomik
from atomik._atomik import Mode


def test__atomik(file_name):
    path = Path(file_name)
    with atomik(path) as f:
        assert not path.exists()

    assert path.exists()



def test__atomik_folder(folder):
    file_1 = "data_1.csv"
    file_2 = "data_2.csv"
    with atomik(Path(folder), mode=Mode.DIR) as path:
        path_1 = Path(path, file_1)
        with open(path_1, 'w') as f:
            print("data_1", file=f)
        path_2 = Path(path, file_2)
        with open(path_2, 'w') as f:
            print("data_2", file=f)

        assert not Path(folder, file_1).exists()
        assert not Path(folder, file_2).exists()

    assert Path(folder, file_1).exists()
    assert Path(folder, file_2).exists()
