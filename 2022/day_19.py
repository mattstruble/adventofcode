# -*- coding: utf-8 -*-
import math
from collections import defaultdict, deque
from copy import deepcopy
from enum import IntEnum
from typing import Set

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

        # print("FACTORY", self.blueprint_id, self.remaining_time, self.robots)

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
        return f"Factory({self.blueprint_id=}, {self.remaining_time=}, {self.stockpile=}, {self.robots=})"

    def __repr__(self) -> str:
        return str(self)

    @memoize
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
        return self.remaining_time > 0 and all(
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
        return self

    def get_buildable_robots(self) -> Iterable[Materials]:
        return filter(lambda r: self.can_build(r), reversed(self.BUILD_PRIORITY))

    def get_future_buildable_robots(self) -> list[Materials]:
        return filter(
            lambda r: self.time_to_build(r) < self.remaining_time,
            reversed(self.BUILD_PRIORITY),
        )

    @staticmethod
    @memoize
    def get_fastest_robot_build(
        factory: "Factory", material: Materials, allow_multiple=False
    ) -> list["Factory"]:
        if factory.remaining_time == 0 or (
            factory.robots[material]["count"] > 0 and not allow_multiple
        ):
            return [factory]

        if material == Materials.OR:
            fastest_node = deepcopy(factory)
            fastest_node.fast_forward(fastest_node.time_to_build(material))
            if fastest_node.can_build(material):
                fastest_node.build(material)
            return [fastest_node]

        # print(f"GET_FASTEST: {factory=}, {material=}\n")

        required_materials = factory.robots[material]["cost_mat"]

        start_factories: list[Factory] = []
        for mat in required_materials:
            start_factories.extend(Factory.get_fastest_robot_build(factory, mat))

        max_remaining_time = min(
            [
                f.remaining_time - f.time_to_build(material)
                for f in start_factories
                if f.time_to_build(material) > -1
            ]
        )
        # print(material, max_remaining_time, start_factories)
        # print(f"start({material}: {start_factory}, {max_remaining_time}")

        queue = deque(start_factories)
        visited: Set[Factory] = set(start_factories)

        max_remaining_time = 1
        while len(queue) and max_remaining_time > 0:
            node = queue.popleft()

            for mat in required_materials:
                for new_factory in Factory.get_fastest_robot_build(
                    deepcopy(node), mat, True
                ):
                    if new_factory in visited:
                        continue

                    remaining_time = (
                        new_factory.remaining_time - new_factory.time_to_build(material)
                    )
                    if remaining_time >= max_remaining_time:
                        max_remaining_time = max(remaining_time, max_remaining_time)
                        queue.append(new_factory)

            visited.add(node)

        # print(max_time_count)
        fastest_nodes = list(
            filter(
                lambda f: f.remaining_time - f.time_to_build(material)
                >= max_remaining_time,
                visited,
            )
        )
        for fastest_node in fastest_nodes:
            fastest_node.fast_forward(fastest_node.time_to_build(material))
            if fastest_node.can_build(material):
                fastest_node.build(material)

        if len(fastest_nodes):
            max_greedy = max(
                fastest_nodes,
                key=lambda f: Factory.get_greedy_build(f).stockpile[Materials.GEODE],
            )
            fastest_nodes = list(
                filter(
                    lambda f: Factory.get_greedy_build(f).stockpile[Materials.GEODE]
                    >= max_greedy.stockpile[Materials.GEODE],
                    fastest_nodes,
                )
            )

        # print(f"FASTEST {material}: {fastest_node=}\n")
        return fastest_nodes

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

        greedy_factory = Factory.get_greedy_build(factory)
        greedy_factory.stockpile[Materials.GEODE]
        fastest_nodes = Factory.get_fastest_robot_build(factory, Materials.GEODE)

        completed = set()
        visited = set()
        max_seen_geode = 0
        # fastest_nodes = sorted(fastest_nodes, key= lambda f: Factory.get_greedy_build(f).stockpile[Materials.GEODE])
        queue = deque(fastest_nodes)
        while len(queue):
            curr_node = queue.pop()

            # if len(queue) % 10 == 0:
            #     print(len(queue), max_seen_geode)

            if (
                curr_node in visited
                or curr_node.remaining_time <= 0
                or Factory.get_greedy_build(curr_node).stockpile[Materials.GEODE]
                < max_seen_geode
            ):
                continue

            if curr_node.remaining_time >= curr_node.time_to_build(Materials.GEODE) + 1:
                for next_node in Factory.get_fastest_robot_build(
                    deepcopy(curr_node), Materials.GEODE, True
                ):
                    queue.append(next_node)

            greedy_node = Factory.get_greedy_build(curr_node)
            completed.add(greedy_node)
            max_seen_geode = max(greedy_node.stockpile[Materials.GEODE], max_seen_geode)

            visited.add(curr_node)
            visited.add(greedy_node)

        # fastest_geode.fast_forward(fastest_geode.remaining_time)
        print(f"{len(visited)=}")
        return completed

    def puzzle_one(self, data: list[str]) -> int:
        geodes = []
        for factory in self.factory_generator(data, 24):
            max_geode = max(
                [f.stockpile[Materials.GEODE] for f in self.process_factory(factory)]
            )
            geodes.append(max_geode * factory.blueprint_id)
            print(f"{factory.blueprint_id=}: {max_geode}")

        return sum(geodes)

    def puzzle_one_example_solution(self) -> Any:
        return 33


Day19(True)
