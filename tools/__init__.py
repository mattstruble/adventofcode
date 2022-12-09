# -*- coding: utf-8 -*-
import os
import re
import sys
from math import sqrt
from typing import Any, Callable, Iterable, List, Tuple, Union


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


def clamp(
    n: Union[int, float], smallest: Union[int, float], largest: Union[int, float]
) -> Union[int, float]:
    return max(smallest, min(n, largest))


INPUTS_DIR = os.path.join(os.path.dirname(sys.argv[0]), "inputs")
os.makedirs(INPUTS_DIR, exist_ok=True)

INPUT_FILE_NAME = "input.txt"
EXAMPLE_FILE_NAME = "example.txt"

CACHE_DIR = os.path.join(os.path.dirname(INPUTS_DIR), ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)

SOLUTION_DIR = os.path.join(os.path.dirname(INPUTS_DIR), "solutions")
os.makedirs(SOLUTION_DIR, exist_ok=True)

LETTERS = "abcdefghijklmnopqrstuvwxyz"
NUMBERS = "0123456789"

UP, RIGHT, DOWN, LEFT = ORTHO_DIRS = (
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
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
ALL_DIRS = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if not x == y == 0]
