# -*- coding: utf-8 -*-
import math
from typing import Optional, Protocol, Union


def clamp(
    n: Union[int, float], smallest: Union[int, float], largest: Union[int, float]
) -> Union[int, float]:
    return max(smallest, min(n, largest))


class Point:
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
        elif type(other) is (float, int):
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
        return type(other) is (Point, Shape) and self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return type(other) is (Point, Shape) and self.x < other.x and self.y < other.y

    def __le__(self, other):
        return type(other) is (Point, Shape) and self.x <= other.x and self.y <= other.y

    def __gt__(self, other):
        return type(other) is (Point, Shape) and self.x > other.x and self.y > other.y

    def __ge__(self, other):
        return type(other) is (Point, Shape) and self.x >= other.x and self.y >= other.y

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
        return f"Point({self.x=}, {self.y=})"

    def __repr__(self) -> str:
        return str(self)


class Shape(Protocol):
    x: int
    y: int

    def contains(self, other: object) -> bool:
        pass

    @property
    def top(self) -> int:
        pass

    @property
    def bottom(self) -> int:
        pass

    @property
    def left(self) -> int:
        pass

    @property
    def right(self) -> int:
        pass

    @property
    def center(self) -> Point:
        return Point((self.left + self.right) // 2, (self.top + self.bottom) // 2)


class Circle(Shape):
    def __init__(
        self, x: int, y: int, radius: float, distance_str="manhattan", grid=True
    ):
        self.x = x
        self.y = y
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

    def __add__(self, other) -> "Circle":
        if isinstance(other, Point):
            return Circle(self.x + other.x, self.y + other.y, self.radius)
        elif isinstance(other, (float, int)):
            return Circle(self.x + other, self.y + other, self.radius)

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.radius))

    def __str__(self) -> str:
        return f"Circle({self.x=}, {self.y=}, {self.radius=})"

    def __repr__(self) -> str:
        return str(self)


class Square(Shape):
    def __init__(self, bottom_left: Point, width: int, height: int):
        self.x = bottom_left.x
        self.y = bottom_left.y
        self.width = width
        self.height = height

    @staticmethod
    def from_corners(
        top_left: Point, top_right: Point, bottom_right: Point, bottom_left: Point
    ) -> "Square":
        return Square(
            bottom_left=bottom_left,
            width=abs(bottom_left.x - bottom_right.x),
            height=abs(top_left.y - bottom_left.y),
        )

    @staticmethod
    def from_edges(top: int, right: int, bottom: int, left: int) -> "Square":
        return Square(Point(left, bottom), abs(right - left), abs(bottom - top))

    @property
    def bottom_left(self):
        return Point(self.x, self.y)

    @property
    def top_right(self):
        return self.bottom_left + Point(self.width, -self.height)

    @property
    def top_left(self):
        return self.bottom_left + Point(0, -self.height)

    @property
    def bottom_right(self):
        return self.bottom_left + Point(self.width, 0)

    def __add__(self, other) -> "Square":
        if isinstance(other, Point):
            return Square(self.bottom_left + other, self.width, self.height)

    def contains(self, other: Union[Point, Circle, "Square"]) -> bool:
        if isinstance(other, Point):
            return (
                self.left <= other.x <= self.right
                and self.top <= other.y <= self.bottom
            )
        if isinstance(other, Square):
            return (
                self.top_left.x <= other.bottom_right.x
                and self.bottom_right.x >= other.bottom_left.x
                and self.top_left.y <= other.bottom_right.y
                and self.bottom_right.y >= other.top_left.y
            )
        if isinstance(other, ComplexShape):
            return other.contains(self)

    @property
    def top(self) -> int:
        return self.bottom_left.y - self.height

    @property
    def bottom(self) -> int:
        return self.bottom_left.y

    @property
    def left(self) -> int:
        return self.bottom_left.x

    @property
    def right(self) -> int:
        return self.bottom_left.x + self.width

    def __hash__(self) -> int:
        return hash((self.bottom_left, self.width, self.height))

    def __str__(self) -> str:
        return f"Square({self.bottom_left=}, {self.width=}, {self.height=})"

    def __repr__(self) -> str:
        return str(self)


class ComplexShape(Shape):
    def __init__(self, shapes):
        self.shapes = shapes

        self.x = sum([shape.x for shape in shapes]) // len(shapes)
        self.y = sum([shape.y for shape in shapes]) // len(shapes)

    @property
    def right(self):
        return max(shape.right for shape in self.shapes)

    @property
    def left(self):
        return min(shape.left for shape in self.shapes)

    @property
    def top(self):
        return min(shape.top for shape in self.shapes)

    @property
    def bottom(self):
        return max(shape.bottom for shape in self.shapes)

    @property
    def bounding_box(self):
        return Square.from_edges(self.top, self.right, self.bottom, self.left)

    def contains(self, other: Union[Point, Circle, Square, "ComplexShape"]):
        if isinstance(other, ComplexShape):
            return self.bounding_box.contains(other.bounding_box) and any(
                shape.contains(oshape)
                for shape in self.shapes
                for oshape in other.shapes
            )
        elif isinstance(other, Point):
            return (
                self.left <= other.x <= self.right
                and self.top <= other.y <= self.bottom
                and any([shape.contains(other) for shape in self.shapes])
            )
        elif isinstance(other, Square):
            return self.bounding_box.contains(other) and any(
                shape.contains(other) for shape in self.shapes
            )
        else:
            return any(shape.contains(other) for shape in self.shapes)

    def __add__(self, other):
        return ComplexShape([shape + other for shape in self.shapes])

    def __hash__(self) -> int:
        return hash(tuple(self.shapes))

    def __str__(self) -> str:
        return f"ComplexShape({self.center=}, \"{', '.join([str(shape) for shape in self.shapes])}\")"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ComplexShape) and hash(self) == hash(other)
