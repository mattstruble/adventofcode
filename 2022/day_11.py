# -*- coding: utf-8 -*-
from dataclasses import dataclass

from tools import *
from tools.alg import *
from tools.runner import PuzzleRunner


class Monkey:
    pass


def mult(a, b):
    return a * b


def sub(a, b):
    return a - b


def add(a, b):
    return a + b


def div(a, b):
    return a / b


OPERATOR_MAP = {"*": mult, "-": sub, "+": add, "/": div}


@dataclass
class Operation:
    left: Union[str, int]
    operator: str
    right: Union[str, int]

    def execute(self, val: int) -> int:
        if self.left == "old":
            a = val
        else:
            a = int(self.left)
        if self.right == "old":
            b = val
        else:
            b = int(self.right)

        return OPERATOR_MAP[self.operator](a, b)


class Day11(PuzzleRunner):
    def puzzle_one_example_solution(self) -> Any:
        return 10605

    def puzzle_one(self, data: list[str]) -> int:
        monkeys = []
        curr_monkey = None
        for line in data:
            if line.startswith("Monkey"):
                if curr_monkey is not None:
                    monkeys.append(curr_monkey)

                curr_monkey = Monkey()
                curr_monkey.id = str_to_ints(line)[0]
                curr_monkey.inspected_cnt = 0
            elif line.strip().startswith("Starting items"):
                curr_monkey.items = str_to_ints(line)
            elif line.strip().startswith("Operation:"):
                line = line[line.find("=") + 1 :].strip()
                print(line.split(" "))
                left, operator, right = line.split(" ")
                curr_monkey.operation = Operation(left, operator, right)
            elif line.strip().startswith("Test:"):
                curr_monkey.test = str_to_ints(line)[0]
            elif line.strip().startswith("If true:"):
                curr_monkey.true_target = str_to_ints(line)[0]
            elif line.strip().startswith("If false:"):
                curr_monkey.false_target = str_to_ints(line)[0]

        monkeys.append(curr_monkey)

        monkeys = sorted(monkeys, key=lambda x: x.id)
        print(len(monkeys), monkeys)

        for rounds in range(20):
            for monkey in monkeys:
                while len(monkey.items):
                    item = monkey.items.pop(0)
                    item = monkey.operation.execute(item)
                    item = item // 3

                    if item % monkey.test == 0:
                        monkeys[monkey.true_target].items.append(item)
                    else:
                        monkeys[monkey.false_target].items.append(item)

                    monkey.inspected_cnt += 1

        min_heap = MinHeap(max_size=2)

        for monkey in monkeys:
            min_heap.push(monkey.inspected_cnt)

        return min_heap[0] * min_heap[1]

    def puzzle_two_example_solution(self) -> Any:
        return 2713310158

    def puzzle_two(self, data: list[str]) -> int:
        monkeys = []
        curr_monkey = None
        for line in data:
            if line.startswith("Monkey"):
                if curr_monkey is not None:
                    monkeys.append(curr_monkey)

                curr_monkey = Monkey()
                curr_monkey.id = str_to_ints(line)[0]
                curr_monkey.inspected_cnt = 0
            elif line.strip().startswith("Starting items"):
                curr_monkey.items = str_to_ints(line)
            elif line.strip().startswith("Operation:"):
                line = line[line.find("=") + 1 :].strip()
                left, operator, right = line.split(" ")
                curr_monkey.operation = Operation(left, operator, right)
            elif line.strip().startswith("Test:"):
                curr_monkey.test = str_to_ints(line)[0]
            elif line.strip().startswith("If true:"):
                curr_monkey.true_target = str_to_ints(line)[0]
            elif line.strip().startswith("If false:"):
                curr_monkey.false_target = str_to_ints(line)[0]

        monkeys.append(curr_monkey)

        monkeys = sorted(monkeys, key=lambda x: x.id)

        modulo = 1
        for monkey in monkeys:
            modulo *= monkey.test

        for rounds in range(10_000):
            if rounds % 100 == 0:
                print(rounds)
            for monkey in monkeys:
                monkey.inspected_cnt += len(monkey.items)
                map_items = list(
                    map(lambda x: monkey.operation.execute(x) % modulo, monkey.items)
                )
                true_items = filter(lambda x: x % monkey.test == 0, map_items)
                false_items = filter(lambda x: x % monkey.test != 0, map_items)

                monkeys[monkey.true_target].items.extend(true_items)
                monkeys[monkey.false_target].items.extend(false_items)

                monkey.items.clear()

        min_heap = MinHeap(max_size=2)

        for monkey in monkeys:
            min_heap.push(monkey.inspected_cnt)

        return min_heap[0] * min_heap[1]


Day11()
