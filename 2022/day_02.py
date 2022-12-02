from dataclasses import dataclass
from enum import Enum
from common import file_line_generator

class Moves(Enum):
    ROCK = 1
    PAPER = 2
    SCISSOR = 3

    def __lt__(self, other): 
        return self.value == (other.value - 1 if other.value > 1 else 3)

MOVE_MAP = {
    "A": Moves.ROCK,
    "B": Moves.PAPER,
    "C": Moves.SCISSOR,
    "X": Moves.ROCK,
    "Y": Moves.PAPER,
    "Z": Moves.SCISSOR
}

def puzzle_one():
    score = 0 
    for line in file_line_generator(__file__):
        opponent_str, my_str = line.split(" ")
        opponent_move = MOVE_MAP[opponent_str]
        my_move = MOVE_MAP[my_str]

        if my_move > opponent_move:
            score += 6
        elif my_move == opponent_move:
            score += 3

        score += my_move.value

    return score 

if __name__ == "__main__":
    print(puzzle_one())
