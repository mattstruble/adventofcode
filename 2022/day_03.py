# -*- coding: utf-8 -*-
from tools.runner import PuzzleRunner


def get_priority(item):
    if ord(item) < 91:
        return ord(item) - ord("A") + 27
    else:
        return ord(item) - ord("a") + 1


class Day3(PuzzleRunner):
    def get_example_str(self) -> str:
        return """
                vJrwpWtwJgWrhcsFMMfFFhFp
                jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
                PmmdzqPrVvPwwTWBwg
                wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
                ttgJtRGJQctTZtZT
                CrZsJsPPZsGzwwsLwLmpwMDw
                """

    def puzzle_one(self, data) -> int:
        priority = 0

        for line in data:
            compartment_one = set([])
            compartment_two = set([])

            for item in line[: len(line) // 2]:
                compartment_one.add(item)

            for item in line[len(line) // 2 :]:
                if item in compartment_one and item not in compartment_two:
                    priority += get_priority(item)

                compartment_two.add(item)

        return priority

    def puzzle_two(self, data) -> int:
        priority = 0
        groups = {}
        curr_group = 0
        for line in data:
            group = set([])
            for item in line:
                if curr_group == 0 or item in groups[curr_group - 1]:
                    group.add(item)

            if curr_group == 2:
                priority += get_priority(group.pop())

            groups[curr_group] = group
            curr_group = (curr_group + 1) % 3

        return priority


Day3()
