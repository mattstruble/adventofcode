# -*- coding: utf-8 -*-
from tools import *
from tools.alg import *
from tools.runner import PuzzleRunner


class Day14(PuzzleRunner):
    def draw_grid(self, rocks: set[Point], sands: set[Point]) -> None:
        minmax_x_rocks = minmax([rock.x for rock in rocks])
        minmax_y_rocks = minmax([rock.y for rock in rocks])
        minmax_x_sand = minmax([sand.x for sand in sands])
        minmax_y_sand = minmax([sand.y for sand in sands])

        min_x, max_x = min(minmax_x_rocks[0], minmax_x_sand[0]), max(
            minmax_x_rocks[1], minmax_x_sand[1]
        )
        min_y, max_y = min(minmax_y_rocks[0], minmax_y_sand[0]), max(
            minmax_y_rocks[1], minmax_y_sand[1]
        )

        for y in range(min_y, max_y + 1):
            row = ""
            for x in range(min_x, max_x + 1):
                if Point(x, y) in sands:
                    row += "o"
                elif Point(x, y) in rocks:
                    row += "#"
                else:
                    row += "."
            print(row)

        input("next")

    def extract_rock_paths(self, data: list[str]) -> set[Point]:
        def str_to_point(string: str) -> Point:
            ints = str_to_ints(string)
            return Point(ints[0], ints[1])

        rocks = set([])
        for line in data:
            point_split = line.split(" -> ")
            points = [str_to_point(split) for split in point_split]
            curr_point = points[0]
            rocks.add(curr_point)

            for dest_point in points[1:]:
                direction = (dest_point - curr_point).normalise()

                while curr_point != dest_point:
                    curr_point = curr_point + direction
                    rocks.add(curr_point)

        return rocks

    def get_sand_locs(
        self,
        rocks: set[Point],
        min_x: int,
        max_x: int,
        max_y: int,
        floor=Point(0, float("inf")),
    ) -> set[Point]:
        sands = set([])
        sand_source = Point(500, 0)
        curr_sand = sand_source
        while (
            min_x < curr_sand.x < max_x
            and curr_sand.y < max_y
            and sand_source not in rocks
        ):
            next_sand = curr_sand + DOWN

            if next_sand in rocks:
                dl = curr_sand + DOWN_LEFT
                dr = curr_sand + DOWN_RIGHT

                if dl not in rocks:
                    next_sand = dl
                elif dr not in rocks:
                    next_sand = dr

            if next_sand in rocks or next_sand.y >= floor.y:
                sands.add(curr_sand)
                rocks.add(curr_sand)
                curr_sand = sand_source
            else:
                curr_sand = next_sand

        return sands

    def puzzle_one(self, data: list[str]) -> int:
        rocks = self.extract_rock_paths(data)
        min_x, max_x = minmax([point.x for point in rocks])
        min_y, max_y = minmax([point.y for point in rocks])

        return len(self.get_sand_locs(rocks, min_x, max_x, max_y))

    def puzzle_one_example_solution(self) -> Any:
        return 24

    def puzzle_two(self, data: list[str]) -> int:
        rocks = self.extract_rock_paths(data)
        min_y, max_y = minmax([point.y for point in rocks])

        return len(
            self.get_sand_locs(
                rocks, float("-inf"), float("inf"), max_y + 2, floor=Point(0, max_y + 2)
            )
        )

    def puzzle_two_example_solution(self) -> Any:
        return 93


Day14()
