import os
import shutil
import uuid

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
    return   str(uuid.uuid4())




@pytest.fixture(autouse=True, scope="session")
def cleanup():
    os.mkdir(WORKING_DIR)
    yield
    shutil.rmtree(WORKING_DIR, ignore_errors=True)
