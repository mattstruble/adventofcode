# -*- coding: utf-8 -*-
from tools.runner import PuzzleRunner


class Day5(PuzzleRunner):
    def get_example_str(self) -> str:
        return """    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

    def puzzle_one(self, data: list[str]) -> int:
        stacks = {}
        pos_lookup = {}
        stacks_reversed = False
        for line in data:
            # construct stacks
            if not line.startswith("move"):
                for i, c in enumerate(line):
                    if c.isalpha() and ord(c) != 32:
                        if i not in stacks:
                            stacks[i] = []

                        stacks[i].append(c)
                    elif c.isdigit():
                        pos_lookup[c] = i
            elif line.startswith("move"):
                if not stacks_reversed:
                    for key, stack in stacks.items():
                        stacks[key] = list(reversed(stack))
                    stacks_reversed = True

                split = line.split(" ")
                number = split[1]
                source = split[3]
                target = split[5]

                for _ in range(int(number)):
                    create = stacks[pos_lookup[source]].pop(-1)
                    stacks[pos_lookup[target]].append(create)

        result = []
        for stack, pos in pos_lookup.items():
            result.append((stack, stacks[pos][-1]))

        return result

    def puzzle_two(self, data: list[str]) -> int:
        stacks = {}
        pos_lookup = {}
        stacks_reversed = False
        for line in data:
            # construct stacks
            if not line.startswith("move"):
                for i, c in enumerate(line):
                    if c.isalpha() and ord(c) != 32:
                        if i not in stacks:
                            stacks[i] = []

                        stacks[i].append(c)
                    elif c.isdigit():
                        pos_lookup[c] = i
            elif line.startswith("move"):
                if not stacks_reversed:
                    for key, stack in stacks.items():
                        stacks[key] = list(reversed(stack))
                    stacks_reversed = True

                split = line.split(" ")
                number = split[1]
                source = split[3]
                target = split[5]

                crates = stacks[pos_lookup[source]][-(int(number)) :]
                stacks[pos_lookup[target]].extend(crates)
                stacks[pos_lookup[source]] = stacks[pos_lookup[source]][
                    : -(int(number))
                ]

        result = []
        for stack, pos in pos_lookup.items():
            result.append((stack, stacks[pos][-1]))

        return result


Day5()
