# -*- coding: utf-8 -*-
from tools import ORTHO_DIRS, Any
from tools.math import Point
from tools.runner import PuzzleRunner


class Day18(PuzzleRunner):
    def get_example_str(self) -> str:
        return """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

    def extract_points(self, data: list[str]) -> list[Point]:
        for line in data:
            coords = line.split(",")
            yield Point(*(int(c) for c in coords), labels="xyz")

    def get_surface_area(self, data: list[str]) -> int:
        exposed_areas = []
        closed_areas = set()
        for point in self.extract_points(data):
            closed_areas.add(point)

            for direction in ORTHO_DIRS + (Point(0, 0, 1), Point(0, 0, -1)):
                adj = point + direction
                if adj not in (closed_areas):
                    exposed_areas.append(point + direction)

        return list(filter(lambda p: p not in closed_areas, exposed_areas))

    def puzzle_one(self, data: list[str]) -> int:
        res = self.get_surface_area(data)
        return len(res)

    def puzzle_one_example_solution(self) -> Any:
        return 64

    def puzzle_two(self, data: list[str]) -> int:
        return super().puzzle_two(data)

    def puzzle_two_example_solution(self) -> Any:
        return super().puzzle_two_example_solution()


Day18()
