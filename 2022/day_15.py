# -*- coding: utf-8 -*-
from typing import Set

from tools import ALL_DIRS, Any, List, Tuple, str_to_ints
from tools.math import Circle, Point
from tools.runner import PuzzleRunner


class Day15(PuzzleRunner):
    def get_sensors_beacons_min_max(
        self, data: list[str]
    ) -> Tuple[List[Circle], Set[Point], int, int]:
        min_x, max_x = float("inf"), float("-inf")
        sensors = []
        beacons = set([])
        for line in data:
            line_split = line.split(":")
            sensor_vals = str_to_ints(line_split[0])
            beacon_vals = str_to_ints(line_split[1])

            sensor_point = Point(sensor_vals[0], sensor_vals[1])
            beacon_point = Point(beacon_vals[0], beacon_vals[1])
            sensor = Circle.from_two_points(sensor_point, beacon_point)

            sensors.append(sensor)
            beacons.add(beacon_point)

            min_x = min(min_x, min(sensor.x - sensor.radius, beacon_point.x))
            max_x = max(max_x, max(sensor.x + sensor.radius, beacon_point.x))

        return sensors, beacons, min_x, max_x

    def get_coverage(
        self,
        row: int,
        sensors: List[Circle],
        beacons: Set[Point],
        min_x: int,
        max_x: int,
    ):
        points = [Point(x, row) for x in range(int(min_x), int(max_x) + 1)]
        sensors = list(
            filter(lambda sensor: sensor.contains(Point(sensor.x, row)), sensors)
        )

        coverage = list(filter(lambda p: any([s.contains(p) for s in sensors]), points))
        return coverage

    def puzzle_one(self, data: list[str]) -> int:
        if self.is_test:
            row = 10
        else:
            row = 2000000

        sensors, beacons, min_x, max_x = self.get_sensors_beacons_min_max(data)
        coverage = self.get_coverage(row, sensors, beacons, min_x, max_x)
        coverage = list(
            filter(
                lambda p: p not in beacons
                and any([p != Point(s.x, s.y) for s in sensors]),
                coverage,
            )
        )

        return len(self.get_coverage(row, sensors, beacons, min_x, max_x))

    def puzzle_one_example_solution(self) -> Any:
        return 26

    def puzzle_two(self, data: list[str]) -> int:
        if self.is_test:
            bounds = (0, 20)
        else:
            bounds = (0, 4000000)

        sensors, beacons, min_x, max_x = self.get_sensors_beacons_min_max(data)
        seen_points = set([])
        for sensor in sensors:
            for dx in range(sensor.radius + 1):
                dy = (sensor.radius) - dx

                beacon = None
                for sign in [Point(x, y) for x in [-1, 1] for y in [-1, 1]]:
                    x = sensor.x + (dx * sign.x)
                    y = sensor.y + (dy * sign.y)

                    edge = Point(x, y)

                    edge_points = []
                    for neighbor in ALL_DIRS:
                        point = edge + neighbor
                        if (
                            sensor.contains(point)
                            or point in seen_points
                            or not (bounds[0] <= point.x <= bounds[1])
                            or not (bounds[0] <= point.y <= bounds[1])
                        ):
                            continue

                        edge_points.append(point)

                    for point in edge_points:
                        if any(filter(lambda s: s.contains(point), sensors)):
                            seen_points.add(point)
                        else:
                            return (point.x * 4000000) + point.y

        return (beacon.x * 4000000) + beacon.y

    def puzzle_two_example_solution(self) -> Any:
        return 56000011


Day15()
