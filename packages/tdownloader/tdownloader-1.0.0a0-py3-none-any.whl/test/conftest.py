""" Test fixtures. """
from pathlib import Path

import pytest


@pytest.fixture
def input_file():
    """ A sample test file for download. """
    path = Path(__file__).parent / Path("data/test_1.txt")
    return str(path)


