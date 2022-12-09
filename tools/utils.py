# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
from typing import AnyStr, Generator

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
