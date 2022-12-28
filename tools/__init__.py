# -*- coding: utf-8 -*-
import os
import re
import sys
from math import sqrt
from typing import Any, Callable, Iterable, List, Tuple, Union

from tools.math import Circle, Point, clamp


def str_to_ints(string: str) -> List[int]:
    return list(map(int, re.findall(r"(-?\d+).?", string)))


def data_to_grid(
    data: Iterable, cast: Callable = None
) -> Tuple[List[List[Any]], int, int]:
    grid = []
    for line in data:
        if cast is not None:
            cols = [cast(c) for c in line]
        else:
            cols = [c for c in line]
        grid.append(cols)

    return grid, len(grid), len(grid[0])


def iord(c) -> int:
    return ord(c.lower()) - ord("a")


def ichr(i) -> str:
    return chr(ord("a") + i)


def distance(p1, p2) -> float:
    return sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))


def cmp(x, y):
    return (x > y) - (x < y)


def minmax(arr: list[Any]) -> Tuple[Any, Any]:
    return min(arr), max(arr)


def arr_to_key(arr: list[Any]) -> str:
    return ",".join(sorted(arr))


UP, RIGHT, DOWN, LEFT = ORTHO_DIRS = (
    Point(0, -1),
    Point(1, 0),
    Point(0, 1),
    Point(-1, 0),
)

DOWN_LEFT = DOWN + LEFT
DOWN_RIGHT = DOWN + RIGHT
UP_LEFT = UP + LEFT
UP_RIGHT = UP + RIGHT

DIRS = {
    "N": UP,
    "E": RIGHT,
    "S": DOWN,
    "W": LEFT,
    "U": UP,
    "R": RIGHT,
    "L": LEFT,
    "D": DOWN,
    "NE": UP + RIGHT,
    "NW": UP + LEFT,
    "SE": DOWN + RIGHT,
    "SW": DOWN + LEFT,
    "UR": UP + RIGHT,
    "UL": UP + LEFT,
    "DR": DOWN + RIGHT,
    "DL": DOWN + LEFT,
}
ALL_DIRS = [Point(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if not x == y == 0]


INPUTS_DIR = os.path.join(os.path.dirname(sys.argv[0]), "inputs")
os.makedirs(INPUTS_DIR, exist_ok=True)

INPUT_FILE_NAME = "input.txt"
EXAMPLE_FILE_NAME = "example.txt"

CACHE_DIR = os.path.join(os.path.dirname(INPUTS_DIR), ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)

LETTERS = "abcdefghijklmnopqrstuvwxyz"
NUMBERS = "0123456789"


class ImmutableList(list):
    def append(self, object: object) -> list:
        new_list = list(self.copy())
        new_list.append(object)

        return ImmutableList(new_list)

    def remove(self, __value: object) -> list:
        new_list = list(self.copy())
        new_list.remove(object)

        return ImmutableList(new_list)


def subsets(collection: Iterable, k: int) -> Iterable:
    yield from partition(collection, k, k)


def partition(collection: Iterable, min: int, k: int) -> Iterable:
    if len(collection) == 1:
        yield [collection]
        return

    first = collection[0]
    for smaller in partition(collection[1:], min - 1, k):
        if len(smaller) > k:
            continue

        if len(smaller) >= min:
            for n, subset in enumerate(smaller):
                yield smaller[:n] + [[first] + subset] + smaller[n + 1 :]

        if len(smaller) < k:
            yield [[first]] + smaller
