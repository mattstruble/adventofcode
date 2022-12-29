# -*- coding: utf-8 -*-
from itertools import cycle

from tools import DOWN, LEFT, RIGHT, UP, Any, Point, Tuple
from tools.math import ComplexShape, Shape, Square
from tools.runner import PuzzleRunner

SHAPES = ["-", "+", "⅃", "I", "■"]


def shape_factory(shape_str: str, loc: Point) -> Shape:
    if shape_str == "-":
        return Square(bottom_left=loc, width=3, height=0)
    elif shape_str == "I":
        return Square(bottom_left=loc, width=0, height=3)
    elif shape_str == "■":
        return Square(bottom_left=loc, width=1, height=1)
    elif shape_str == "⅃":
        bottom_square = Square(bottom_left=loc, width=2, height=0)
        right_square = Square(bottom_left=loc + (RIGHT * 2), width=0, height=2)
        return ComplexShape([bottom_square, right_square])
    elif shape_str == "+":
        vertical = Square(bottom_left=loc + RIGHT, width=0, height=2)
        horizontal = Square(bottom_left=loc + UP, width=2, height=0)
        return ComplexShape([vertical, horizontal])

    raise ValueError(f"Unknown shape: {shape_str}")


jet_to_dir = {"<": LEFT, ">": RIGHT}


class Day17(PuzzleRunner):
    @staticmethod
    def move_shape(shape: Shape, chamber: Square, direction: Point):
        new_shape = shape + direction
        ret_shape = shape

        # print(f"NEW_SHAPE: left {new_shape.left()}, right {new_shape.right()}, width: {chamber.width}, contains {any(placed.contains(shape) for placed in placed_shapes)}")
        if (
            0 <= new_shape.left
            and new_shape.right < chamber.width
            and not any(placed.contains(new_shape) for placed in chamber.placed_shapes)
        ):
            ret_shape = new_shape

        # print(f"MOVING SHAPE:\n\t{shape=}, \n\t{direction=}, \n\t{new_shape=}, \n\t{ret_shape=}")

        return ret_shape

    @staticmethod
    def visualize(chamber: Square, shape: Shape):
        print(Day17.get_recent_formation(chamber, shape))
        input("continue?")

    @staticmethod
    def get_chamber(width=7, height=0) -> Square:
        return Square(Point(0, 0), width=width, height=height)

    @staticmethod
    def get_recent_formation(chamber: Square, shape: Shape = None) -> str:
        rows = []
        min_y = chamber.top - 3
        max_y = min(0, chamber.top + 20)
        for y in range(min_y, max_y + 1):
            row_str = ""
            for x in range(chamber.width):
                if any(
                    placed.contains(Point(x, y)) for placed in chamber.placed_shapes
                ):
                    row_str += "#"
                elif shape and shape.contains(Point(x, y)):
                    row_str += "@"
                else:
                    row_str += "."
            rows.append(row_str)

        return "\n".join(rows)

    def drop_shape(self, chamber, jets, shape_cycle, cache) -> Tuple[bool, int, int]:
        shape_index, shape_str = next(shape_cycle)
        start_point = Point(2, chamber.top - 3)
        shape = shape_factory(shape_str, start_point)

        while True:
            jet_index, jet_str = next(jets)
            shape = self.move_shape(shape, chamber, jet_to_dir[jet_str])
            # self.visualize(chamber, shape)
            new_shape = self.move_shape(shape, chamber, DOWN)

            if new_shape.bottom > 0:
                new_shape = self.move_shape(new_shape, chamber, UP)
                break

            if new_shape == shape:
                break

            shape = new_shape

        chamber.placed_shapes.append(new_shape)
        chamber.height = max(chamber.height, abs(new_shape.top) + 1)

        cache_key = (shape_index, jet_index, self.get_recent_formation(chamber))

        if cache_key in cache:
            height, shape_ct = cache[cache_key]
            return (True, height, shape_ct)
        else:
            cache[cache_key] = (chamber.height, len(chamber.placed_shapes))

        return (False, 0, 0)

    def get_fallen_rocks(self, jets, chamber: Square, num_rocks: int) -> None:
        chamber.placed_shapes = []
        shape_cycle = cycle(enumerate(SHAPES))
        cache = {}

        cache_hit = False
        while not cache_hit:
            cache_hit, cache_height, cache_shape_ct = self.drop_shape(
                chamber, jets, shape_cycle, cache
            )

        height_diff = chamber.height - cache_height
        shapes_diff = len(chamber.placed_shapes) - cache_shape_ct

        remaining_drops = num_rocks - len(chamber.placed_shapes)
        required_repeats = remaining_drops // shapes_diff
        remaining_drops %= shapes_diff

        height_delta = height_diff * required_repeats

        for _ in range(remaining_drops):
            self.drop_shape(chamber, jets, shape_cycle, cache)

        chamber.height += height_delta

    def puzzle_one(self, data: list[str]) -> int:
        jets = cycle(enumerate(next(data)))
        chamber = self.get_chamber()

        self.get_fallen_rocks(jets, chamber, 2022)

        return chamber.height

    def puzzle_one_example_solution(self) -> Any:
        return 3068

    def puzzle_two(self, data: list[str]) -> int:

        jets = cycle(enumerate(next(data)))
        chamber = self.get_chamber()

        self.get_fallen_rocks(jets, chamber, 1000000000000)

        return chamber.height

    def puzzle_two_example_solution(self) -> Any:
        return 1514285714288


Day17()
