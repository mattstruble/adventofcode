# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
from typing import AnyStr, Generator, Optional

from tools import INPUT_FILE_NAME, INPUTS_DIR


def file_line_generator(
    file_path=None, file_name=None, *, path: str = None
) -> Generator[AnyStr, None, None]:
    if file_path is None:
        file_path = sys.argv[0]

    if file_name is None:
        file_name = INPUT_FILE_NAME

    if path is None:
        path = os.path.join(INPUTS_DIR, Path(file_path).stem, file_name)

    if not os.path.exists(path):
        raise FileNotFoundError

    with open(path, "r") as file:
        for line in file:
            yield line.rstrip("\r\n")


class Singleton:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


def get_file_stem(file_path: Optional[str] = None) -> str:
    if file_path is None:
        file_path = sys.argv[0]

    filename = Path(file_path).stem

    return filename


def extract_day_from_path(file_path: Optional[str] = None) -> int:
    return int(get_file_stem(file_path).split("_")[1])


def extract_year_from_path(file_path: Optional[str] = None) -> int:
    if file_path is None:
        file_path = sys.argv[0]

    filename = Path(os.path.dirname(file_path)).stem

    return int(filename)


def memoize(fn):
    memo = {}

    def memoized(*args):
        if args in memo:
            return memo[args]
        else:
            result = fn(*args)
            memo[args] = result
            return result

    return memoized
