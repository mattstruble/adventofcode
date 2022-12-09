# -*- coding: utf-8 -*-
import os
import re
import sys
from typing import List


def str_to_ints(string: str) -> List[int]:
    return list(map(int, re.findall(r"(-?\d+).?", string)))


INPUTS_DIR = os.path.join(os.path.dirname(sys.argv[0]), "inputs")
INPUT_FILE_NAME = "input.txt"

LETTERS = "abcdefghijklmnopqrstuvwxyz"

UP, RIGHT, DOWN, LEFT = VDIRS = (
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
)
DIRS = {"N": UP, "E": RIGHT, "S": DOWN, "W": LEFT}
ALL_DIRS = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if not x == y == 0]
