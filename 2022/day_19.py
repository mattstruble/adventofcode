# -*- coding: utf-8 -*-
import math
from collections import defaultdict, deque
from copy import deepcopy
from enum import IntEnum

from tools import Any, Iterable, dict_to_str, str_to_ints
from tools.runner import PuzzleRunner
from tools.utils import memoize


class Materials(IntEnum):
    OR = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3

    def __repr__(self):
        return str(self)

    def __str__(self) -> str:
        return str(self.value)

    def __lt__(self, other) -> bool:
        if isinstance(other, Materials):
            return self.value < other.value

        return self.value < other


class Factory:
    BUILD_PRIORITY: list[Materials] = [
        Materials.GEODE,
        Materials.OBSIDIAN,
        Materials.CLAY,
        Materials.OR,
    ]

    def __init__(
        self,
        blueprint_id: int,
        remaining_time: int,
        ore_robot_cost: list[int],
        clay_robot_cost: list[int],
        obsidian_robot_cost: list[int],
        geode_robot_cost: list[int],
    ) -> None:

        self.blueprint_id = blueprint_id
        self.remaining_time = remaining_time

        self.robots = {
            Materials.OR: {
                "cost_val": ore_robot_cost,
                "cost_mat": [Materials.OR],
                "count": 1,
            },
            Materials.CLAY: {
                "cost_val": clay_robot_cost,
                "cost_mat": [Materials.OR],
                "count": 0,
            },
            Materials.OBSIDIAN: {
                "cost_val": obsidian_robot_cost,
                "cost_mat": [Materials.OR, Materials.CLAY],
                "count": 0,
            },
            Materials.GEODE: {
                "cost_val": geode_robot_cost,
                "cost_mat": [Materials.OR, Materials.OBSIDIAN],
                "count": 0,
            },
        }

        self.stockpile = defaultdict(lambda: 0)

        print("FACTORY", self.blueprint_id, self.remaining_time, self.robots)

    def __hash__(self):
        return hash(
            (
                self.blueprint_id,
                self.remaining_time,
                dict_to_str(self.stockpile),
                dict_to_str(self.robots),
            )
        )

    def __str__(self) -> str:
        return (
            f"Factory({self.blueprint_id=}, {self.remaining_time=}, {self.stockpile=})"
        )

    def __repr__(self) -> str:
        return str(self)

    def time_to_build(self, robot_name: Materials) -> int:
        robot = self.robots[robot_name]
        if any(self.robots[material]["count"] == 0 for material in robot["cost_mat"]):
            return float("inf")

        costs = []

        for i, material in enumerate(robot["cost_mat"]):
            if (
                self.stockpile[material] > 0
                and self.stockpile[material] < robot["cost_val"][i]
            ):
                cost = math.ceil(
                    (robot["cost_val"][i] - self.stockpile[material])
                    / self.robots[material]["count"]
                )
            elif self.stockpile[material] == 0:
                cost = math.ceil(robot["cost_val"][i] / self.robots[material]["count"])
            else:
                cost = 0

            costs.append(max(0, cost))

        return max(costs)

    def can_build(self, robot_name: Materials) -> bool:
        robot = self.robots[robot_name]
        return all(
            robot["cost_val"][i] <= self.stockpile[material]
            for i, material in enumerate(robot["cost_mat"])
        )

    def build(self, robot_name: Materials) -> None:
        robot = self.robots[robot_name]
        if any(
            robot["cost_val"][i] > self.stockpile[material]
            for i, material in enumerate(robot["cost_mat"])
        ):
            print(
                f"Trying to build unbuildable robot {robot_name}:\n\t{robot=}\n\t{self.stockpile=}"
            )
            return

        for i, material in enumerate(robot["cost_mat"]):
            self.stockpile[material] -= robot["cost_val"][i]

        self.fast_forward(1)

        robot["count"] += 1

    def fast_forward(self, time: int):
        if time > self.remaining_time:
            time = self.remaining_time

        for material, robot in self.robots.items():
            self.stockpile[material] += robot["count"] * time

        self.remaining_time -= time

    def get_buildable_robots(self) -> Iterable[Materials]:
        return filter(lambda r: self.can_build(r), reversed(self.BUILD_PRIORITY))

    def get_future_buildable_robots(self) -> list[Materials]:
        return filter(
            lambda r: self.time_to_build(r) < self.remaining_time,
            reversed(self.BUILD_PRIORITY),
        )

    @staticmethod
    @memoize
    def get_greedy_build(factory: "Factory") -> "Factory":
        if factory.remaining_time <= 0:
            return factory

        factory_copy = deepcopy(factory)

        next_buildable = filter(
            lambda m: factory_copy.time_to_build(m) <= factory_copy.remaining_time,
            Factory.BUILD_PRIORITY,
        )

        try:
            material = next(next_buildable)
            factory_copy.fast_forward(factory_copy.time_to_build(material))
            factory_copy.build(material)
        except StopIteration:
            factory_copy.fast_forward(factory_copy.remaining_time)

        return Factory.get_greedy_build(factory_copy)

    def get_material(self, material: Materials) -> int:
        return self.stockpile[material]


class Day19(PuzzleRunner):
    def get_example_str(self) -> str:
        return """Blueprint 1: Each or robot costs 4 or. Each clay robot costs 2 or. Each obsidian robot costs 3 or and 14 clay. Each geode robot costs 2 or and 7 obsidian.
Blueprint 2: Each or robot costs 2 or. Each clay robot costs 3 or. Each obsidian robot costs 3 or and 8 clay. Each geode robot costs 3 or and 12 obsidian."""

    def factory_generator(self, data: list[str], time) -> Iterable[Factory]:
        for line in data:
            blueprint_split = line.split(":")
            blueprint_id = str_to_ints(blueprint_split[0])[0]
            robots_split = blueprint_split[1].split(".")

            ore_robot_cost = str_to_ints(robots_split[0])
            clay_robot_cost = str_to_ints(robots_split[1])
            obsidian_robot_cost = str_to_ints(robots_split[2])
            geode_robot_cost = str_to_ints(robots_split[3])

            yield Factory(
                blueprint_id=blueprint_id,
                remaining_time=time,
                ore_robot_cost=ore_robot_cost,
                clay_robot_cost=clay_robot_cost,
                obsidian_robot_cost=obsidian_robot_cost,
                geode_robot_cost=geode_robot_cost,
            )

    def process_factory(self, factory: Factory) -> list[Factory]:
        queue = deque([factory])
        finished = []

        greedy_factory = Factory.get_greedy_build(factory)
        max_geode = greedy_factory.stockpile[Materials.GEODE]

        """
        TODO: STore the max_geode and use that to calculate and trim the stack?
        We can calculate the maximum potential geodes of a node and kill it early if it won't break the curr max

        Also, optimize to building out geode smashers, cause a lot of things are finishing with 0 geodes, which defeats
        the purpose if everything is just building clay / or perpetually. It needs to build with purpose.
        """
        while len(queue):
            node = queue.popleft()
            greedy_node = Factory.get_greedy_build(node)

            if greedy_node.stockpile[Materials.GEODE] < max_geode:
                continue

            for buildable in node.get_buildable_robots():
                new_factory = deepcopy(node)
                # print("buildable now")
                new_factory.build(buildable)
                if (
                    Factory.get_greedy_build(new_factory).stockpile[Materials.GEODE]
                    >= max_geode
                ):
                    queue.append(new_factory)

            for future in node.get_future_buildable_robots():
                new_factory = deepcopy(node)
                new_factory.fast_forward(new_factory.time_to_build(future))
                # print("fastforward to future build")
                new_factory.build(future)
                if (
                    Factory.get_greedy_build(new_factory).stockpile[Materials.GEODE]
                    >= max_geode
                ):
                    queue.append(new_factory)

            # if greedy_node.stockpile[Materials.GEODE] > max_geode:
            finished.append(greedy_node)
            max_geode = max(max_geode, greedy_node.stockpile[Materials.GEODE])
            if len(finished) % 10000 == 0:
                print(len(finished), len(queue), max_geode, finished[-1].stockpile)

            # queue = deque(sorted(queue, reverse=True, key=lambda f: Factory.get_greedy_build(f).stockpile[Materials.GEODE]))

        print(max_geode)
        return finished

    def puzzle_one(self, data: list[str]) -> int:
        geodes = []
        for factory in self.factory_generator(data, 24):
            max_geode = max(
                [f.stockpile[Materials.GEODE] for f in self.process_factory(factory)]
            )
            geodes.append(max_geode * factory.blueprint_id)

        return sum(geodes)

    def puzzle_one_example_solution(self) -> Any:
        return 33


Day19(True)
