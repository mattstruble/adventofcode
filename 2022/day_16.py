# -*- coding: utf-8 -*-
import re
from typing import Set

from tools import Any, ImmutableList, Tuple, str_to_ints
from tools.alg import Node
from tools.runner import PuzzleRunner

OPEN_TIME = 1


class Day16(PuzzleRunner):
    def generate_node_graph(self, data: list[str]) -> Tuple[Node, set]:
        pass

        valve_info_dict = {}
        for line in data:
            valve_str, tunnels_str = line.split(";")
            valve_name = re.findall(r"[A-Z][A-Z]", valve_str)[0]
            valve_rate = str_to_ints(valve_str)[0]

            valve = Node(valve_name, value=valve_rate)

            tunnel_nodes = re.findall(r"[A-Z][A-Z]", tunnels_str)

            valve_info_dict[valve_name] = {}
            valve_info_dict[valve_name]["node"] = valve
            valve_info_dict[valve_name]["children"] = tunnel_nodes

        valves = set([])
        for valve_info in valve_info_dict.values():
            valve: Node = valve_info["node"]
            for child_name in valve_info["children"]:
                valve.children[child_name] = valve_info_dict[child_name]["node"]

            valves.add(valve)

        return valve_info_dict["AA"]["node"], valves

    def maximize_release(self, start: Node, valves: Set[Node], time_limit=30) -> int:
        target_valves = list(filter(lambda v: v.value > 0, valves))
        max_pressure = 0

        stack = [[ImmutableList([start]), 0, {}]]

        while len(stack):
            path, minutes_elapesed, opened_valves = stack.pop()
            curr_node = path[-1]

            if minutes_elapesed >= time_limit or len(path) == len(target_valves) + 1:
                pressure = 0

                for valve, time_opened in opened_valves.items():
                    minutes = max(time_limit - time_opened, 0)
                    pressure += valve.value * minutes

                max_pressure = max(max_pressure, pressure)
            else:
                for next_node in target_valves:
                    if next_node not in opened_valves.keys():
                        travel_time = len(Node.BFS(curr_node, next_node)) - 1

                        elapsed_time = minutes_elapesed + travel_time + OPEN_TIME

                        next_open_valves = opened_valves.copy()
                        next_open_valves[next_node] = elapsed_time

                        stack.append(
                            [path.append(next_node), elapsed_time, next_open_valves]
                        )

        return max_pressure

    def puzzle_one(self, data: list[str]) -> int:
        root, nodes = self.generate_node_graph(data)

        return self.maximize_release(root, nodes)

    def puzzle_one_example_solution(self) -> Any:
        return 1651


Day16()
