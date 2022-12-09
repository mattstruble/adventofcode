import os 
import sys 
from pathlib import Path
from typing import Generator, AnyStr
from tools import INPUTS_DIR, INPUT_FILE_NAME

def file_line_generator(file_path=None, *, path:str = None) -> Generator[AnyStr, None, None]:
    if file_path is None:
        file_path = sys.argv[0]

    if path is None:
        path = os.path.join(INPUTS_DIR, Path(file_path).stem, INPUT_FILE_NAME)

    with open(path, 'r') as file:
        for line in file:
            yield line.rstrip("\r\n")

