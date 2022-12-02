from dataclasses import dataclass
from enum import Enum
from common import file_line_generator

class Moves(Enum):
    ROCK = 1
    PAPER = 2
    SCISSOR = 3

    def __lt__(self, other): 
        return self == other - 1 

    def __add__(self, other) -> "Moves":
        if not isinstance(other, (Moves, int)):
            raise ValueError("Expected Moves or Int type.")

        if isinstance(other, Moves):
            other = other.value

        val = self.value + other 

        if val > self.SCISSOR.value:
            return Moves(val % self.SCISSOR.value)
        else:
            return Moves(val)
        
    def __sub__(self, other) -> "Moves": 
        if not isinstance(other, (Moves, int)):
            raise ValueError("Expected Moves or Int type.")

        if isinstance(other, Moves):
            other = other.value

        val = self.value - other 

        return Moves((val if self.value > self.ROCK.value else self.SCISSOR.value))


MOVE_MAP = {
    "A": Moves.ROCK,
    "B": Moves.PAPER,
    "C": Moves.SCISSOR,
}

WIN = 6
DRAW = 3
LOSE = 0

def puzzle_one():
    move_map = {
        "X": Moves.ROCK,
        "Y": Moves.PAPER,
        "Z": Moves.SCISSOR
    }

    move_map = {**MOVE_MAP, **move_map}

    score = 0 
    for line in file_line_generator(__file__):
        opponent_str, my_str = line.split(" ")
        opponent_move = move_map[opponent_str]
        my_move = move_map[my_str]

        if my_move > opponent_move:
            score += WIN
        elif my_move == opponent_move:
            score += DRAW
        else:
            score += LOSE

        score += my_move.value

    return score 

def puzzle_two():
    score = 0 
    for line in file_line_generator(__file__):
        opponent_str, my_str = line.split(" ")
        opponent_move = MOVE_MAP[opponent_str]

        if my_str == "X":
            my_move = opponent_move - 1 
            score += LOSE
        elif my_str == "Y":
            my_move = opponent_move
            score += DRAW
        else:
            my_move = opponent_move + 1
            score += WIN

        score += my_move.value

    return score 

if __name__ == "__main__":
    print(puzzle_one())
    print(puzzle_two())
