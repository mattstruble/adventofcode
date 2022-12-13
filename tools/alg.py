# -*- coding: utf-8 -*-
import heapq
from math import sqrt
from typing import Any, Optional, Union

from tools import clamp


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

    def manhatten(self, other) -> int:
        if not isinstance(other, Point):
            raise ValueError(
                f"Cannot calculate the distance between Point and [{type(other)}]"
            )

        return sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2))

    def chebyshev(self, other) -> int:
        if not isinstance(other, Point):
            raise ValueError(
                f"Cannot calculate the distance between Point and [{type(other)}]"
            )

        return max(abs(self.x - other.x), abs(self.y - other.y))

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __repr__(self) -> str:
        return str(self)


UP, RIGHT, DOWN, LEFT = ORTHO_DIRS = (
    Point(0, -1),
    Point(1, 0),
    Point(0, 1),
    Point(-1, 0),
)
DIRS = {
    "N": UP,
    "E": RIGHT,
    "S": DOWN,
    "W": LEFT,
    "U": UP,
    "R": RIGHT,
    "L": LEFT,
    "D": DOWN,
}
ALL_DIRS = [Point(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if not x == y == 0]


class MinHeap:
    def __init__(self, max_size: Optional[int] = None):
        self.max_size = max_size
        self.heap = []

    def push(self, x: Any):
        if self.max_size and len(self) >= self.max_size:
            heapq.heappushpop(self.heap, x)
        else:
            heapq.heappush(self.heap, x)

    def pop(self):
        return heapq.heappop(self.h)

    def peak(self):
        return self.heap[0]

    def __getitem__(self, i) -> Any:
        return self.heap[i]

    def __len__(self):
        return len(self.heap)

    def __str__(self) -> str:
        return str(self.heap)


class MaxHeap(MinHeap):
    class Comparator:
        def __init__(self, val):
            self.val = val

        def __lt__(self, other):
            return self.val > self.other

        def __eq__(self, other):
            return self.val == self.other

        def __str__(self):
            return str(self.val)

    def push(self, x: Any):
        return super().push(MaxHeap.Comparator(x))

    def pop(self):
        return super().pop().val

    def peak(self):
        return super().peak().val

    def __getitem__(self, i) -> Any:
        return super().__getitem__(i).val


class Node:
    def __init__(
        self,
        name,
        *,
        value=None,
        children: dict[str, "Node"] = None,
        parent: "Node" = None,
    ) -> None:
        self.name = name
        self.parent = parent
        self.children = children if children else {}
        self.value = value

    def sum_values(self) -> int:
        if self.value:
            return self.value

        return sum([child.sum_values() for child in self.children.values()])

    def up(self) -> "Node":
        return self.parent

    def down(self, name) -> "Node":
        return self.children[name]

    def add_child(self, name, value=None, children=None):
        self.children[name] = Node(
            name=name, value=value, children=children, parent=self
        )

    def has_children(self) -> bool:
        return len(self.children) > 0

    def __str__(self) -> str:
        return f"{self.name}:{self.value}"

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def iterator(root: "Node"):
        queue = [root]
        visited = set([])
        while queue:
            node = queue.pop()

            if node not in visited:
                yield node

                queue.extend(node.children.values())
