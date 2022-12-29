# -*- coding: utf-8 -*-
from itertools import cycle

from tools import DOWN, LEFT, RIGHT, UP, Any, Point
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
    def move_shape(
        shape: Shape, chamber: Square, placed_shapes: list[Shape], direction: Point
    ):
        new_shape = shape + direction
        ret_shape = shape

        # print(f"NEW_SHAPE: left {new_shape.left()}, right {new_shape.right()}, width: {chamber.width}, contains {any(placed.contains(shape) for placed in placed_shapes)}")
        if (
            0 <= new_shape.left
            and new_shape.right < chamber.width
            and not any(placed.contains(new_shape) for placed in placed_shapes)
        ):
            ret_shape = new_shape

        # print(f"MOVING SHAPE:\n\t{shape=}, \n\t{direction=}, \n\t{new_shape=}, \n\t{ret_shape=}")

        return ret_shape

    @staticmethod
    def visualize(chamber: Square, placed_shapes: list[Shape], shape: Shape):
        min_y = min([shape.top for shape in placed_shapes + [shape]])

        for y in range(min_y, 1, 1):
            row_str = ""
            for x in range(chamber.width):
                if shape.contains(Point(x, y)):
                    row_str += "@"
                elif any([placed.contains(Point(x, y)) for placed in placed_shapes]):
                    row_str += "#"
                else:
                    row_str += "."
            print(row_str)

        input("continue?")

    @staticmethod
    def get_chamber(width=7, height=float("-inf")) -> Square:
        return Square(Point(0, 0), width=width, height=height)

    def get_fallen_rocks(self, jets, chamber: Square, num_rocks: int) -> list[Shape]:
        start_point = Point(2, -3)
        placed_shapes = []
        shape_cycle = cycle(SHAPES)

        for _ in range(num_rocks):
            shape = shape_factory(next(shape_cycle), start_point)
            # print("START", shape)

            while shape.bottom <= 0:
                shape = self.move_shape(
                    shape, chamber, placed_shapes, jet_to_dir[next(jets)]
                )
                # self.visualize(chamber, placed_shapes, shape)
                new_shape = self.move_shape(shape, chamber, placed_shapes, DOWN)

                if new_shape == shape:
                    break
                elif new_shape.bottom > 0:
                    new_shape = self.move_shape(new_shape, chamber, [], UP)
                    break

                shape = new_shape

            # print("END", new_shape)
            placed_shapes.append(new_shape)
            start_point = Point(2, min(start_point.y, new_shape.top - 4))

        return placed_shapes

    def puzzle_one(self, data: list[str]) -> int:
        jets = cycle(next(data))
        chamber = self.get_chamber()

        fallen_rocks = self.get_fallen_rocks(jets, chamber, 2022)

        return abs(min(rock.top for rock in fallen_rocks)) + 1

    def puzzle_one_example_solution(self) -> Any:
        return 3068


Day17()
