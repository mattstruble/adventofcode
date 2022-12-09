from tools.runner import PuzzleRunner

def get_assignments(line: str) -> list[tuple]:
    assignments = line.split(",")
    result = []
    for assignment in assignments:
        sections = assignment.split("-")
        result.append((int(sections[0]), int(sections[1])))

    return result 


class Day4(PuzzleRunner):

    def get_example_str(self) -> str:
        return """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

    def puzzle_one(self, data: list[str]) -> int:
        result = 0
        for line in data: 
            first_assignment, second_assignment = get_assignments(line)
            if first_assignment[0] <= second_assignment[0] and first_assignment[1] >= second_assignment[1]:
                result += 1
            elif second_assignment[0] <= first_assignment[0] and second_assignment[1] >= first_assignment[1]:
                result += 1
        return result 


    def puzzle_two(self, data: list[str]) -> int:
        result = 0
        for line in data:
            first_assignment, second_assignment = get_assignments(line)
            if (first_assignment[0] <= second_assignment[1] and first_assignment[0] >= second_assignment[0]) \
                or (second_assignment[0] <= first_assignment[1] and second_assignment[0] >= first_assignment[0]):
                result += 1

        return result 


Day4()