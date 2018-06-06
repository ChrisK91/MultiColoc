# pylint: disable=W0621
"""
Test file helper functions
"""


import os
import os.path
from pytest import fixture
from colocalizer.helper_functions import get_append_or_write

@fixture
def csvfile(tmpdir):
    """
    Fixture to create a temprorary path to a csv file
    The file will not exist, and be deleted if it exists

    returns path to a not existing csv-file
    """

    path = tmpdir.join("tmp.csv")

    if os.path.isfile(path):
        os.remove(path)

    return path

def test_write(csvfile):
    """
    Test on non existing file
    """

    assert get_append_or_write(csvfile) == "w"

def test_append(csvfile):
    """
    Test on existing file
    """

    csvfile.write("temporary_file")
    assert get_append_or_write(csvfile) == "a"
