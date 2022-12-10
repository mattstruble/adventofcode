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
    def get_example_str(self) -> str:
        return """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

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
