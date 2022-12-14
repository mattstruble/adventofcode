# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime
from typing import Any, Optional

from tools import CACHE_DIR
from tools.utils import (
    extract_day_from_path,
    extract_year_from_path,
    file_line_generator,
    get_file_stem,
)
from tools.web import AOCWebInterface

SOLUTIONS_FILE = os.path.join(CACHE_DIR, "solutions.json")


class PuzzleRunner:
    def __init__(self, test_only=False) -> None:
        self._puzzle_funcs = [self.puzzle_one, self.puzzle_two]
        self._example_solutions = [
            self.puzzle_one_example_solution,
            self.puzzle_two_example_solution,
        ]

        self.name = get_file_stem()
        self.day = extract_day_from_path()
        self.year = extract_year_from_path()

        self.solutions = self._load_solutions()

        self.aoc = AOCWebInterface(self.year, self.day)
        self.aoc.download_input()
        self.aoc.download_prompt()
        self.aoc.download_examples()

        self.run(test_only)

    def _load_solutions(self) -> dict:
        try:
            with open(SOLUTIONS_FILE, "r") as f:
                solutions = json.load(f)
        except FileNotFoundError:
            solutions = {}

        return solutions

    def _save(
        self, func_name: str, result: Any, correct: bool, test_result: Any = None
    ) -> None:
        self.solutions[func_name] = {
            "timestamp": str(datetime.now()),
            "solution": result,
            "correct": correct,
            "test_result": test_result,
        }

        with open(SOLUTIONS_FILE, "w") as f:
            json.dump(self.solutions, f)

    def get_example_str(self) -> str:
        raise NotImplementedError

    def get_example(self, puzzle_num=1) -> list[str]:
        try:
            return [
                item for item in self.get_example_str().split("\n") if len(item) > 0
            ]
        except NotImplementedError:
            while puzzle_num > 0:
                try:
                    return file_line_generator(file_name=f"EXAMPLE_{puzzle_num}.txt")
                except FileNotFoundError:
                    puzzle_num -= 1

        raise NotImplementedError

    def puzzle_one_example_solution(self) -> Any:
        return None

    def puzzle_one(self, data: list[str]) -> int:
        raise NotImplementedError

    def puzzle_two(self, data: list[str]) -> int:
        raise NotImplementedError

    def puzzle_two_example_solution(self) -> Any:
        return None

    def _run_puzzle(self, puzzle_func, data_generator) -> Optional[Any]:
        try:
            result = puzzle_func(data_generator())
        except NotImplementedError:
            result = "Not Implemented"
        except FileNotFoundError:
            result = "No test file."

        return result

    def run(self, test_only: bool = False):
        for i, puzzle_func in enumerate(self._puzzle_funcs):
            func_name = puzzle_func.__qualname__

            if func_name in self.solutions and self.solutions[func_name]["correct"]:
                print(
                    f"{func_name} already ran successfully: {self.solutions[func_name]['timestamp']}"
                )
                continue

            if (
                i > 0
                and not self.solutions[self._puzzle_funcs[i - 1].__qualname__][
                    "correct"
                ]
            ):
                break  # break if previous puzzle is wrong

            self.is_test = True
            test_results = self._run_puzzle(
                puzzle_func=puzzle_func, data_generator=self.get_example
            )
            print(f"TEST {func_name}: {test_results}")

            if not test_only:
                self.is_test = False
                run_results = self._run_puzzle(
                    puzzle_func=puzzle_func, data_generator=file_line_generator
                )
                print(f"RUN {func_name}: {run_results}")

                if (
                    self._example_solutions[i]() == test_results
                    or input(f"Submit result {run_results}? (y/n)") == "y"
                ):
                    print("Submitting")
                    correct = self.aoc.submit(i + 1, run_results)
                    print("Correct!" if correct else "Wrong!")

                    self._save(func_name, run_results, correct, test_results)

            self.aoc.download_prompt(i + 1)
            self.aoc.download_examples(i + 1)
