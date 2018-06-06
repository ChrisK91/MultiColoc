"""
Test distance measurements
"""

from colocalizer.helper_functions import distance

def test_distance_horizontal():
    """
    Test horizontal points, second point is right
    to first point
    """

    p1 = (0, 0)
    p2 = (0, 1)

    assert distance(p1, p2) == 1

def test_distance_vertical():
    """
    Test vertical points, second point is above
    first point
    """

    p1 = (0, 0)
    p2 = (1, 0)

    assert distance(p1, p2) == 1

def test_distance_horizontal_reverse():
    """
    Test horizontal points, second point is right
    to first point
    """

    p1 = (0, 1)
    p2 = (0, 0)

    assert distance(p1, p2) == 1

def test_distance_vertical_reverse():
    """
    Test vertical points, second point is below
    first point
    """

    p1 = (1, 0)
    p2 = (0, 0)

    assert distance(p1, p2) == 1
