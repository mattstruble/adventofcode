# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
from typing import AnyStr, Generator, Optional

from tools import INPUT_FILE_NAME, INPUTS_DIR


def file_line_generator(
    file_path=None, *, path: str = None
) -> Generator[AnyStr, None, None]:
    if file_path is None:
        file_path = sys.argv[0]

    if path is None:
        path = os.path.join(INPUTS_DIR, Path(file_path).stem, INPUT_FILE_NAME)

    with open(path, "r") as file:
        for line in file:
            yield line.rstrip("\r\n")


class Singleton:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


def extract_day_from_path(file_path: Optional[str] = None) -> int:
    if file_path is None:
        file_path = sys.argv[0]

    filename = Path(file_path).stem

    return int(filename.split("_")[1])


def extract_year_from_path(file_path: Optional[str] = None) -> int:
    if file_path is None:
        file_path = sys.argv[0]

    filename = Path(os.path.dirname(file_path)).stem

    return int(filename)
