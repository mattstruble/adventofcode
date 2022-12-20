# -*- coding: utf-8 -*-
import math
from typing import Optional, Union


def clamp(
    n: Union[int, float], smallest: Union[int, float], largest: Union[int, float]
) -> Union[int, float]:
    return max(smallest, min(n, largest))


class Point:
    x: int
    y: int

    def __init__(self, x: Union[int, tuple], y: Optional[int] = None):
        if isinstance(x, tuple) and y is not None:
            raise ValueError("X cannot be a tuple, and pass in y.")
        if isinstance(x, tuple) and y is None:
            self.x = x[0]
            self.y = x[1]
        elif y is not None:
            self.x = x
            self.y = y

    def __sub__(self, other) -> "Point":
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        elif isinstance(other, (float, int)):
            return Point(self.x - other, self.y - other)

    def __add__(self, other) -> "Point":
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        elif isinstance(other, (float, int)):
            return Point(self.x + other, self.y + other)

    def __mul__(self, other) -> "Point":
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)
        elif isinstance(other, (float, int)):
            return Point(self.x * other, self.y * other)

    def __truediv__(self, other) -> "Point":
        if isinstance(other, Point):
            return Point(self.x / other.x, self.y / other.y)
        elif isinstance(other, (float, int)):
            return Point(self.x / other, self.y / other)

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def normalise(self) -> "Point":
        return Point(clamp(self.x, -1, 1), clamp(self.y, -1, 1))

    def manhatten(self, other) -> float:
        if not isinstance(other, Point):
            raise ValueError(
                f"Cannot calculate the distance between Point and [{type(other)}]"
            )
        diff = self - other
        return sum((abs(diff.x), abs(diff.y)))

    def chebyshev(self, other) -> int:
        if not isinstance(other, Point):
            raise ValueError(
                f"Cannot calculate the distance between Point and [{type(other)}]"
            )

        return max(abs(self.x - other.x), abs(self.y - other.y))

    def distance(self, other, distance_str="manhattan") -> float:
        if distance_str == "manhattan" or distance_str == "m":
            distance_func = self.manhatten
        elif distance_str == "chebyshev" or distance_str == "c":
            distance_func = self.chebyshev
        else:
            raise ValueError(
                f'Distance must be one of the following: "manhattan", "m", "chebyshev", "c"'
            )

        return distance_func(other)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __repr__(self) -> str:
        return str(self)


class Circle(Point):
    def __init__(
        self, x: int, y: int, radius: float, distance_str="manhattan", grid=True
    ):
        super().__init__(x, y)
        self.radius = abs(radius)

        self.grid = grid
        self.distance_str = distance_str

    @staticmethod
    def from_two_points(center: Point, edge: Point, distance_str="manhattan"):
        return Circle(center.x, center.y, abs(center.distance(edge, distance_str)))

    def contains(self, point: Point) -> bool:
        if self.grid:
            return math.ceil(self.distance(point, self.distance_str)) <= math.ceil(
                self.radius
            )
        else:
            return self.distance(point, self.distance_str) <= self.radius

    def __eq__(self, other):
        return (
            isinstance(other, Circle)
            and self.x == other.x
            and self.y == other.y
            and self.radius == other.radius
        )

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.radius))

    def __str__(self) -> str:
        return f"Circle({self.x}, {self.y}, {self.radius})"
