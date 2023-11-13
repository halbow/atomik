import os
import shutil

import pytest

WORKING_DIR = "./tests/TEST_DATA"


@pytest.fixture
def file_name():
    return f"{WORKING_DIR}/test_file.txt"


@pytest.fixture
def folder():
    return "{WORKING_DIR}"


@pytest.fixture(autouse=True, scope="session")
def cleanup():
    os.mkdir(WORKING_DIR)
    yield
    shutil.rmtree(WORKING_DIR, ignore_errors=True)
