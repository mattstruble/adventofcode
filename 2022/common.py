import os 
import sys 
import requests
from typing import Generator, AnyStr, Optional, Any, Iterable, List

import heapq
from pathlib import Path
from functools import lru_cache

import configparser
import re 

INPUTS_DIR = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE_NAME = "input.txt"

LETTERS = "abcdefghijklmnopqrstuvwxyz"

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
DIRS = {'N': UP, 'E': RIGHT, 'S': DOWN, 'W': LEFT }
ALL_DIRS = [(x, y) for x in [-1,0,1] for y in [-1,0,1] if not x == y == 0]

def str_to_ints(string: str) -> List[int]:
    return map(int, re.findall(r'(-?\d+).?', string))

@lru_cache(maxsize=1)
def get_configuration() ->configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "puzzle.cfg"))

    return config 

def download_input(file_path:Optional[str]=None): 
    if file_path is None:
        file_path = sys.argv[0]

    filename = Path(file_path).stem

    if os.path.exists(os.path.join(INPUTS_DIR, filename, INPUT_FILE_NAME)):
        return 

    input_num = int(filename.split("_")[1])

    config = get_configuration()
    cookies = {}
    for key, value in config.items("requests.cookies"):
        cookies[key] = value
        

    response = requests.get(f"https://adventofcode.com/2022/day/{input_num}/input", cookies=cookies)

    os.makedirs(os.path.join(INPUTS_DIR, filename), exist_ok=True)

    with open(os.path.join(INPUTS_DIR, filename, INPUT_FILE_NAME), 'wb') as f:
        f.write(response.content)

def file_line_generator(file_path=None, *, path:str = None) -> Generator[AnyStr, None, None]:
    if file_path is None:
        file_path = sys.argv[0]

    if path is None:
        path = os.path.join(INPUTS_DIR, Path(file_path).stem, INPUT_FILE_NAME)

    with open(path, 'r') as file:
        for line in file:
            yield line.rstrip("\r\n")

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

    def __getitem__(self, i) -> Any: 
        return self.heap[i]

    def __len__(self):
        return len(self.heap)

    def __str__(self) -> str:
        return str(self.heap)

class PuzzleRunner: 

    def __init__(self) -> None:
        self._puzzle_funcs = [
            self.puzzle_one,
            self.puzzle_two
        ]

        download_input()

        self.test()
        self.run()

    def get_example_str(self) -> str: 
        raise NotImplementedError

    @lru_cache(maxsize=1)
    def get_example(self) -> list[str]:
        return [item for item in self.get_example_str().split("\n") if len(item) > 0]

    def puzzle_one(self, data: list[str]) -> int:
        raise NotImplementedError

    def puzzle_two(self, data: list[str]) -> int:
        raise NotImplementedError

    def _run_puzzle(self, data_generator) -> None:
        for puzzle_func in self._puzzle_funcs:
            try: 
                result = puzzle_func(data_generator())
                print(f"{puzzle_func.__qualname__}: {result}")
            except NotImplementedError: 
                print(f"{puzzle_func.__qualname__} not Implemented")

    def run(self):
        print("\nRUN")
        try:
            self._run_puzzle(file_line_generator)
        except FileNotFoundError:
            print("No test file.")

    def test(self):
        print("\nTEST")
        self._run_puzzle(self.get_example)