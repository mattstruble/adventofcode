# -*- coding: utf-8 -*-
import json

from tools import *
from tools.alg import *
from tools.runner import PuzzleRunner


class Day13(PuzzleRunner):
    def puzzle_one_example_solution(self) -> Any:
        return 13

    def extract_packets(self, data) -> List[List[int]]:
        packets = []
        for line in data:
            if len(line):
                packets.append(json.loads(line))

        return packets

    def compare_packets(self, left: Union[list, int], right: Union[list, int]) -> bool:
        if type(left) is int and type(right) is int:
            return cmp(left, right)

        for l_item, r_item in zip(left, right):
            if type(l_item) != type(r_item):
                l_item = [l_item] if type(l_item) is int else l_item
                r_item = [r_item] if type(r_item) is int else r_item

            cmp_result = self.compare_packets(l_item, r_item)

            if cmp_result != 0:
                return cmp_result

        return cmp(len(left), len(right))

    def puzzle_one(self, data: list[str]) -> int:
        packets = self.extract_packets(data)
        correct_sum = 0
        for i in range(0, len(packets), 2):
            left = packets[i]
            right = packets[i + 1]

            if self.compare_packets(left, right) <= 0:
                # print(f"CORRECT[{(i+1)//2}]:\n\t{left}\n\t{right}")
                correct_sum += i // 2 + 1

        return correct_sum

    def puzzle_two_example_solution(self) -> Any:
        return 140

    def puzzle_two(self, data: list[str]) -> int:
        packets = self.extract_packets(data)

        def count_lower(divider):
            return sum(self.compare_packets(packet, divider) < 0 for packet in packets)

        return (count_lower([[2]]) + 1) * (count_lower([[6]]) + 2)


Day13()
