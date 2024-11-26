import math
from typing import Dict, Union, Tuple

class GeometricCalculator:
    @staticmethod
    def circle_area(radius: float) -> float:
        """Calculate the area of a circle."""
        if radius < 0:
            raise ValueError("Radius cannot be negative")
        return math.pi * radius ** 2

    @staticmethod
    def circle_perimeter(radius: float) -> float:
        """Calculate the perimeter (circumference) of a circle."""
        if radius < 0:
            raise ValueError("Radius cannot be negative")
        return 2 * math.pi * radius

    @staticmethod
    def rectangle_area(length: float, width: float) -> float:
        """Calculate the area of a rectangle."""
        if length < 0 or width < 0:
            raise ValueError("Length and width cannot be negative")
        return length * width

    @staticmethod
    def rectangle_perimeter(length: float, width: float) -> float:
        """Calculate the perimeter of a rectangle."""
        if length < 0 or width < 0:
            raise ValueError("Length and width cannot be negative")
        return 2 * (length + width)

    @staticmethod
    def triangle_area(base: float, height: float) -> float:
        """Calculate the area of a triangle."""
        if base < 0 or height < 0:
            raise ValueError("Base and height cannot be negative")
        return 0.5 * base * height

    @staticmethod
    def triangle_perimeter(side1: float, side2: float, side3: float) -> float:
        """Calculate the perimeter of a triangle."""
        if side1 < 0 or side2 < 0 or side3 < 0:
            raise ValueError("Sides cannot be negative")
        # Check triangle inequality theorem
        if (side1 + side2 <= side3) or (side2 + side3 <= side1) or (side1 + side3 <= side2):
            raise ValueError("Invalid triangle sides")
        return side1 + side2 + side3

    @staticmethod
    def sphere_volume(radius: float) -> float:
        """Calculate the volume of a sphere."""
        if radius < 0:
            raise ValueError("Radius cannot be negative")
        return (4/3) * math.pi * radius ** 3

    @staticmethod
    def cylinder_volume(radius: float, height: float) -> float:
        """Calculate the volume of a cylinder."""
        if radius < 0 or height < 0:
            raise ValueError("Radius and height cannot be negative")
        return math.pi * radius ** 2 * height

    @staticmethod
    def cone_volume(radius: float, height: float) -> float:
        """Calculate the volume of a cone."""
        if radius < 0 or height < 0:
            raise ValueError("Radius and height cannot be negative")
        return (1/3) * math.pi * radius ** 2 * height

    @staticmethod
    def cube_volume(side: float) -> float:
        """Calculate the volume of a cube."""
        if side < 0:
            raise ValueError("Side length cannot be negative")
        return side ** 3
