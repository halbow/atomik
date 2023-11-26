import shutil
import uuid
from pathlib import Path

import pytest

WORKING_DIR = "./tests/TEST_DATA"


@pytest.fixture
def folder():
    return f"{WORKING_DIR}/{uuid.uuid4()}"


@pytest.fixture
def file_name():
    return f"{WORKING_DIR}/test_file_{uuid.uuid4()}.txt"


@pytest.fixture
def data():
    return f"data_start_{uuid.uuid4()}_data_end"


@pytest.fixture(autouse=True)
def cleanup():
    Path(WORKING_DIR).mkdir(exist_ok=True)
    Path(WORKING_DIR, ".tmp").mkdir(exist_ok=True)
    yield
    shutil.rmtree(WORKING_DIR, ignore_errors=True)
