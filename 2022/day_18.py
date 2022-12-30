# -*- coding: utf-8 -*-
from typing import Set, Tuple

from tools import ORTHO_DIRS, Any, minmax
from tools.math import Point
from tools.runner import PuzzleRunner

ORTHO_3D = ORTHO_DIRS + (Point(0, 0, 1), Point(0, 0, -1))


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

    def get_exposed_sides(self, data: list[str]) -> Tuple[list[Point], Set[Point]]:
        exposed_areas = []
        closed_areas = set()
        for point in self.extract_points(data):
            closed_areas.add(point)

            for direction in ORTHO_3D:
                adj = point + direction
                if adj not in (closed_areas):
                    exposed_areas.append(point + direction)

        return (
            list(filter(lambda p: p not in closed_areas, exposed_areas)),
            closed_areas,
        )

    def puzzle_one(self, data: list[str]) -> int:
        exposed, _ = self.get_exposed_sides(data)
        return len(exposed)

    def puzzle_one_example_solution(self) -> Any:
        return 64

    @staticmethod
    def point_in_cube(
        point: Point,
        min_x: int,
        max_x: int,
        min_y: int,
        max_y: int,
        min_z: int,
        max_z: int,
    ) -> int:
        """Return -1 if outside, 0 on edge, or 1 inside"""

        if (
            min_x <= point.x <= max_x
            and min_y <= point.y <= max_y
            and min_z <= point.z <= max_z
        ):
            if (
                point.x == min_x
                or point.x == max_x
                or point.y == min_y
                or point.y == max_y
                or point.z == min_z
                or point.z == max_z
            ):
                return 0
            else:
                return 1

        return -1

    def puzzle_two(self, data: list[str]) -> int:
        exposed, obsidian = self.get_exposed_sides(data)

        min_x, max_x = minmax([p.x for p in exposed])
        min_y, max_y = minmax([p.y for p in exposed])
        min_z, max_z = minmax([p.z for p in exposed])

        def point_filter(p: Point):
            return self.point_in_cube(p, min_x, max_x, min_y, max_y, min_z, max_z)

        surface_access = set()
        visited = set()
        exposed_set = set(exposed)

        for point in exposed_set:
            if point in visited:
                continue

            queue = [point]
            current_visited = set()
            on_edge = False
            while len(queue):
                node = queue.pop()

                if node in current_visited:
                    continue

                if point_filter(node) == 0:
                    on_edge = True

                neighbors = filter(
                    lambda p: p not in obsidian and point_filter(p) > -1,
                    [node + direction for direction in ORTHO_3D],
                )
                queue.extend(neighbors)
                current_visited.add(node)

            visited.update(current_visited)
            if on_edge:
                surface_access.update(current_visited)

        return len(list(filter(lambda p: p in surface_access, exposed)))

    def puzzle_two_example_solution(self) -> Any:
        return 58


Day18()
