# -*- coding: utf-8 -*-
import itertools
import math
from typing import Protocol, Union


def clamp(
    n: Union[int, float], smallest: Union[int, float], largest: Union[int, float]
) -> Union[int, float]:
    return max(smallest, min(n, largest))


class Point:
    def __init__(self, *coordinates, labels=None):
        self.coordinates = tuple(coordinates)
        self.labels = labels

    def __iter__(self):
        return (x for x in self.coordinates)

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self.coordinates[index])
        if isinstance(index, int):
            return self.coordinates[index]

        raise TypeError(
            f"{cls.__name__} indices must be integers or slices, not {type(index).__name__}"
        )

    def __getattr__(self, name):
        if self.labels and len(name) == 1:
            l = self.labels.find(name)
            if 0 <= l <= len(self.coordinates):
                return self.coordinates[l]

        raise AttributeError(
            f"{type(self).__name__} object doesn't have attribute {name}"
        )

    def __setattr__(self, name, value):
        if len(name) == 1:
            if self.labels is not None and name in self.labels:
                raise AttributeError(f"readonly attribute {name}")
            elif name.islower():
                raise AttributeError(
                    f"cannot set attribute 'a' to 'z' in {type(self).__name__}"
                )

        super().__setattr__(name, value)

    def __len__(self):
        return len(self.coordinates)

    def __sub__(self, other) -> "Point":
        if isinstance(other, Point):
            label = (
                self.labels
                if (other.labels is None or len(other) < len(self))
                else other.labels
            )
            return Point(
                *(a - b for a, b in itertools.zip_longest(self, other, fillvalue=0)),
                labels=label,
            )
        elif isinstance(other, (float, int)):
            return Point(x - other for x in self)

        return NotImplemented

    def __rsub__(self, other) -> "Point":
        return -(self - other)

    def __neg__(self) -> "Point":
        return Point(-x for x in self)

    def __add__(self, other) -> "Point":
        if isinstance(other, Point):
            label = (
                self.labels
                if (other.labels is None or len(other) < len(self))
                else other.labels
            )
            return Point(
                *(a + b for a, b in itertools.zip_longest(self, other, fillvalue=0)),
                labels=label,
            )
        elif type(other) is (float, int):
            return Point(x + other for x in self)

        return NotImplemented

    def __radd__(self, other) -> "Point":
        return self + other

    def __mul__(self, other) -> "Point":
        if isinstance(other, Point):
            label = (
                self.labels
                if (other.labels is None or len(other) < len(self))
                else other.labels
            )
            return Point(
                *(a * b for a, b in itertools.zip_longest(self, other, fillvalue=1)),
                labels=label,
            )
        elif isinstance(other, (float, int)):
            return Point(x * other for x in self)

        return NotImplemented

    def __rmul__(self, other) -> "Point":
        return self * other

    def __truediv__(self, other) -> "Point":
        if isinstance(other, Point):
            label = (
                self.labels
                if (other.labels is None or len(other) < len(self))
                else other.labels
            )
            return Point(
                *(a / b for a, b in itertools.zip_longest(self, other, fillvalue=1)),
                labels=label,
            )
        elif isinstance(other, (float, int)):
            return Point(x / other for x in self)

        return NotImplemented

    def __rtruediv__(self, other) -> "Point":
        return self // other

    def __div__(self, other) -> "Point":
        if isinstance(other, Point):
            label = (
                self.labels
                if (other.labels is None or len(other) < len(self))
                else other.labels
            )
            return Point(
                *(a // b for a, b in itertools.zip_longest(self, other, fillvalue=1)),
                labels=label,
            )
        elif isinstance(other, (float, int)):
            return Point(x // other for x in self)

        return NotImplemented

    def __rdiv__(self, other) -> "Point":
        return self // other

    def __eq__(self, other):
        return (
            isinstance(other, Point)
            and len(self) == len(other)
            and all(a == b for a, b in zip(self, other))
        )

    def __lt__(self, other):
        return (
            isinstance(other, Point)
            and len(self) == len(other)
            and all(a < b for a, b in zip(self, other))
        )

    def __le__(self, other):
        return (
            isinstance(other, Point)
            and len(self) == len(other)
            and all(a <= b for a, b in zip(self, other))
        )

    def __gt__(self, other):
        return (
            isinstance(other, Point)
            and len(self) == len(other)
            and all(a > b for a, b in zip(self, other))
        )

    def __ge__(self, other):
        return (
            isinstance(other, Point)
            and len(self) == len(other)
            and all(a >= b for a, b in zip(self, other))
        )

    def normalise(self) -> "Point":
        return Point(clamp(x, -1, 1) for x in self)

    def manhatten(self, other) -> float:
        if not isinstance(other, Point):
            raise ValueError(
                f"Cannot calculate the distance between Point and [{type(other)}]"
            )
        diff = self - other
        return sum((abs(x) for x in diff))

    def chebyshev(self, other) -> int:
        if not isinstance(other, Point):
            raise ValueError(
                f"Cannot calculate the distance between Point and [{type(other)}]"
            )

        return max(abs(a - b for a, b in zip(self, other)))

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
        return hash(tuple(self.coordinates))

    def __str__(self) -> str:
        return f"Point({','.join(str(x) for x in self.coordinates)})"

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
