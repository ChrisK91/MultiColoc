from colocalizer import colocalize
from structures import Options

from numpy.testing import assert_array_equal

from skimage.io import imread

def test_mask_generation(tmpdir):
    options = Options(None, None, str(tmpdir), 1, 0, ".tif")

    fileoptions = [
        ("tests/testfiles/source/Test Cases.tif", None, str(tmpdir.join("1.tif")), "ch1"),
        ("tests/testfiles/source/Test Cases-1.tif", None, str(tmpdir.join("2.tif")), "ch2"),
        ("tests/testfiles/source/Test Cases-2.tif", None, str(tmpdir.join("3.tif")), "ch3")
    ]

    colocalize.new_run()
    colocalize.spatial_colocalize(fileoptions, options)

    expected_first = imread("tests/testfiles/expected/Test Cases.tif")
    expected_second = imread("tests/testfiles/expected/Test Cases-1.tif")
    expected_third = imread("tests/testfiles/expected/Test Cases-2.tif")

    assert_array_equal(imread(str(tmpdir.join("1.tif"))) > 0, expected_first > 0)
    assert_array_equal(imread(str(tmpdir.join("2.tif"))) > 0, expected_second > 0)
    assert_array_equal(imread(str(tmpdir.join("3.tif"))) > 0, expected_third > 0)