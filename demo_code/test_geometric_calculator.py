import pytest
import math
from geometric_calculator import GeometricCalculator

@pytest.fixture
def calculator():
    return GeometricCalculator()

def test_circle_calculations(calculator):
    # Test area
    assert calculator.circle_area(1) == pytest.approx(math.pi)
    assert calculator.circle_area(2) == pytest.approx(4 * math.pi)
    with pytest.raises(ValueError):
        calculator.circle_area(-1)

    # Test perimeter
    assert calculator.circle_perimeter(1) == pytest.approx(2 * math.pi)
    assert calculator.circle_perimeter(2) == pytest.approx(4 * math.pi)
    with pytest.raises(ValueError):
        calculator.circle_perimeter(-1)

def test_rectangle_calculations(calculator):
    # Test area
    assert calculator.rectangle_area(2, 3) == 6
    assert calculator.rectangle_area(5, 4) == 20
    with pytest.raises(ValueError):
        calculator.rectangle_area(-2, 3)
        calculator.rectangle_area(2, -3)

    # Test perimeter
    assert calculator.rectangle_perimeter(2, 3) == 10
    assert calculator.rectangle_perimeter(5, 4) == 18
    with pytest.raises(ValueError):
        calculator.rectangle_perimeter(-2, 3)
        calculator.rectangle_perimeter(2, -3)

def test_triangle_calculations(calculator):
    # Test area
    assert calculator.triangle_area(4, 3) == 6
    assert calculator.triangle_area(5, 2) == 5
    with pytest.raises(ValueError):
        calculator.triangle_area(-4, 3)
        calculator.triangle_area(4, -3)

    # Test perimeter
    assert calculator.triangle_perimeter(3, 4, 5) == 12
    with pytest.raises(ValueError):
        calculator.triangle_perimeter(-3, 4, 5)
        calculator.triangle_perimeter(1, 1, 3)  # Invalid triangle

def test_sphere_volume(calculator):
    assert calculator.sphere_volume(1) == pytest.approx((4/3) * math.pi)
    assert calculator.sphere_volume(2) == pytest.approx((4/3) * math.pi * 8)
    with pytest.raises(ValueError):
        calculator.sphere_volume(-1)

def test_cylinder_volume(calculator):
    assert calculator.cylinder_volume(1, 1) == pytest.approx(math.pi)
    assert calculator.cylinder_volume(2, 3) == pytest.approx(12 * math.pi)
    with pytest.raises(ValueError):
        calculator.cylinder_volume(-1, 1)
        calculator.cylinder_volume(1, -1)

def test_cone_volume(calculator):
    assert calculator.cone_volume(1, 3) == pytest.approx(math.pi)
    assert calculator.cone_volume(2, 3) == pytest.approx(4 * math.pi)
    with pytest.raises(ValueError):
        calculator.cone_volume(-1, 3)
        calculator.cone_volume(1, -3)

def test_cube_volume(calculator):
    assert calculator.cube_volume(1) == 1
    assert calculator.cube_volume(2) == 8
    assert calculator.cube_volume(3) == 27
    with pytest.raises(ValueError):
        calculator.cube_volume(-1)
