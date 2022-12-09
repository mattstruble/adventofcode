from tools import RIGHT, UP, DOWN, LEFT
from tools.runner import PuzzleRunner
from math import sqrt, pow

dir_map = {
    "U": UP, 
    "R": RIGHT, 
    "L": LEFT,
    "D": DOWN
}

def distance(p1, p2) -> int:
    return sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

class Day9(PuzzleRunner):

    def get_example_str(self) -> str:
        return """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

    def puzzle_one(self, data: list[str]) -> int:
        head_pos = prev_head = (0, 0)
        tail_pos = (0, 0)
        tail_visited = set(tail_pos)
        for line in data: 
            direction, steps = line.split(" ")
            direction = dir_map[direction]

            for _ in range(int(steps)):
                head_pos = (head_pos[0] + direction[0], head_pos[1] + direction[1])
                if distance(head_pos, tail_pos) > 1.5:
                    tail_pos = prev_head
                    tail_visited.add(tail_pos)
                
                prev_head = head_pos

        return len(tail_visited)

    def puzzle_two(self, data: list[str]) -> int:
        knots = [(0, 0)] * 10
        prev_positions = [(0, 0)] * 10
        tail_visited = set([knots[-1]])
        
        for line in data: 
            dir_str, steps = line.split(" ")
            direction = dir_map[dir_str]

            for _ in range(int(steps)):
                prev_positions[0] = knots[0]
                knots[0] = (knots[0][0] + direction[0], knots[0][1] + direction[1])

                for i in range(1, len(knots)):
                    if distance(knots[i-1], knots[i]) > 1.5:
                        prev_positions[i] = knots[i]
                        diag =clamp(knots[i-1][0] - knots[i][0], -1, 1), clamp(knots[i-1][1] - knots[i][1], -1, 1)
                        knots[i] = (knots[i][0] + diag[0], knots[i][1] + diag[1])
                    else:
                        break 
                
                tail_visited.add(knots[-1])

        return len(tail_visited)

Day9()
