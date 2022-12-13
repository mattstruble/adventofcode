# -*- coding: utf-8 -*-
from tools import *
from tools.alg import *
from tools.runner import PuzzleRunner


class Day12(PuzzleRunner):
    def puzzle_one_example_solution(self) -> Any:
        return 31

    def dijkstra(self, start, end, grid, rows, cols):
        cost = {}
        queue = [(start, 0)]
        cost[start] = 0

        while len(queue) > 0:
            node, steps = queue.pop(0)
            # print(node, cost)
            if cost[node] != steps:
                continue

            node_iord = iord(grid[node.y][node.x])
            next_steps = steps + 1

            for neighbor in ORTHO_DIRS:
                child = node + neighbor

                # ignore if outside grid
                if child.x < 0 or child.x >= cols or child.y < 0 or child.y >= rows:
                    continue

                # ignore if step is too large
                if iord(grid[child.y][child.x]) - node_iord > 1:
                    continue

                if child not in cost or next_steps < cost[child]:
                    cost[child] = next_steps
                    if child != end:
                        queue.append((child, next_steps))

            queue = sorted(queue, key=lambda x: x[1])

        try:
            return cost[end]
        except KeyError:
            return float("inf")

    def puzzle_one(self, data: list[str]) -> int:
        grid, rows, cols = data_to_grid(data)

        start = end = None
        # Find Start and End
        for y in range(rows):
            for x in range(cols):
                if grid[y][x] == "S":
                    start = Point(x, y)
                    grid[y][x] = "a"
                elif grid[y][x] == "E":
                    end = Point(x, y)
                    grid[y][x] = "z"

            if start != None and end != None:
                break

        return self.dijkstra(start, end, grid, rows, cols)

    def puzzle_two_example_solution(self) -> Any:
        return 29

    def puzzle_two(self, data: list[str]) -> int:
        grid, rows, cols = data_to_grid(data)

        end = None
        starts = []
        for y in range(rows):
            for x in range(cols):
                if grid[y][x] == "S":
                    start = Point(x, y)
                    starts.append(start)
                    grid[y][x] = "a"
                elif grid[y][x] == "E":
                    end = Point(x, y)
                    grid[y][x] = "z"
                elif grid[y][x] == "a":
                    starts.append(Point(x, y))

        smallest_path = float("inf")

        for start in starts:
            cost = self.dijkstra(start, end, grid, rows, cols)
            smallest_path = min(smallest_path, cost)

        return smallest_path


Day12()
