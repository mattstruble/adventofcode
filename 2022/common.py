import os 
import sys 
from typing import Generator, AnyStr, Optional, Any, Iterable

import heapq
from pathlib import Path

INPUTS_DIR = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE_NAME = "input.txt"

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

    def get_example(self) -> Iterable[AnyStr]:
        raise NotImplementedError

    def puzzle_one(self, data: Iterable[str]) -> int:
        raise NotImplementedError

    def puzzle_two(self, data: Iterable[str]) -> int:
        raise NotImplementedError

    def _run(self, data: Iterable[str]) -> None:
        for puzzle_func in self._puzzle_funcs:
            try: 
                result = puzzle_func(data)
                print(f"{puzzle_func.__qualname__}: {result}")
            except NotImplementedError: 
                print(f"{puzzle_func.__qualname__} not Implemented")

    def run(self):
        self._run(file_line_generator())

    def test(self):
        self._run(self.get_example())