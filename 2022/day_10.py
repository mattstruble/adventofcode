# -*- coding: utf-8 -*-
from tools import *
from tools.alg import *
from tools.runner import *


def get_cycles(data):
    cycles = [1]
    X = 1
    for line in data:
        split = line.split(" ")
        command = split[0]
        if len(split) == 2:
            value = int(split[1])
        else:
            value = 0

        if command == "addx":
            cycles.append(X)
            X += value
            cycles.append(X)
        else:
            cycles.append(X)

    return cycles


class Day10(PuzzleRunner):
    def puzzle_one_example_solution(self) -> Any:
        return 13140

    def puzzle_one(self, data: list[str]) -> int:
        cycles = get_cycles(data)
        return sum([cycles[i - 1] * i for i in range(20, len(cycles), 40)])

    def puzzle_two_example_solution(self) -> Any:
        return """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""

    def puzzle_two(self, data: list[str]) -> int:
        cycles = get_cycles(data)

        scanline = ""
        for r in range(6):
            for c in range(40):
                sprite_loc = cycles.pop(0)

                if sprite_loc - 1 <= c <= sprite_loc + 1:
                    scanline += "#"
                else:
                    scanline += "."
            scanline += "\n"

        return scanline


Day10()
