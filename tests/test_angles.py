"""
Tests for the angle function
"""

from colocalizer.helper_functions import angle

def test_angle_horizontal():
    """
    Test two horizontal points
    """

    p1 = (0, 0)
    p2 = (0, 1)

    assert angle(p1, p2) == 0

def test_angle_vertical():
    """
    Test two vertical points
    """

    p1 = (0, 0)
    p2 = (1, 0)

    assert angle(p1, p2) == 90

def test_angle_horizontal_inverse():
    """
    Test, where horizontal points down, where second point is
    left to first point
    """

    p1 = (0, 1)
    p2 = (0, 0)

    assert angle(p1, p2) == 180

def test_angle_vertical_inverse():
    """
    Test second point below first point
    """


    p1 = (1, 0)
    p2 = (0, 0)

    assert angle(p1, p2) == 270

def test_angle_diagonal():
    """
    Test diagonal points
    """

    p1 = (0, 0)
    p2 = (1, 1)

    assert angle(p1, p2) == 45

def test_angle_diagonal_inverse():
    """
    Test diagonal points, where second point is
    bottom left of first point
    """

    p1 = (0, 0)
    p2 = (-1, -1)

    assert angle(p1, p2) == 225
