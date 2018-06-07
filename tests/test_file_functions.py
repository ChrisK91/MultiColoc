# pylint: disable=W0621
"""
Test file helper functions
"""
import os
import os.path
from pytest import fixture
from colocalizer.helper_functions import get_append_or_write, save_binary_image

import numpy as np
from numpy.testing import assert_array_equal

from skimage.io import imread


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

def test_binary_mask_save(tmpdir):
    path = tmpdir.join("stripes.png")
    path = str(path)

    data = np.array([
        [True, True, True],
        [False, False, False],
        [True, True, True]
    ])

    save_binary_image(path, data)

    image = imread(path)

    data_result = image == 65535
    assert_array_equal(data, data_result)