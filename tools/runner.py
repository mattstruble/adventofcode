# -*- coding: utf-8 -*-
from functools import lru_cache

from tools.utils import (
    extract_day_from_path,
    extract_year_from_path,
    file_line_generator,
)
from tools.web import AOCWebInterface


class PuzzleRunner:
    def __init__(self, test_only=False) -> None:
        self._puzzle_funcs = [self.puzzle_one, self.puzzle_two]

        self.day = extract_day_from_path()
        self.year = extract_year_from_path()

        self.aoc = AOCWebInterface(self.year, self.day)
        self.aoc.download_input()

        self.test()
        if not test_only:
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
