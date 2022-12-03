from common import file_line_generator

PUZZLE_ONE_EXAMPLE = [
    "vJrwpWtwJgWrhcsFMMfFFhFp",
    "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
    "PmmdzqPrVvPwwTWBwg",
    "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
    "ttgJtRGJQctTZtZT",
    "CrZsJsPPZsGzwwsLwLmpwMDw"
]

def get_priority(item):
    if ord(item) < 91:
        return (ord(item) - ord("A") + 27) 
    else:
        return (ord(item) - ord("a") + 1)

def puzzle_one(iter):
    priority = 0 

    for line in iter: 
        compartment_one = set([])
        compartment_two = set([])

        for item in line[:len(line)//2]:
            compartment_one.add(item)

        for item in line[len(line)//2:]:
            if item in compartment_one and item not in compartment_two:                
                priority += get_priority(item)

            compartment_two.add(item)

    return priority

def puzzle_two(iter):
    priority = 0 
    groups = {
        -1: set([*"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"])
    }

    curr_group = 0 
    for line in iter: 
        group = set([])
        for item in line: 
            if item in groups[curr_group-1]:
                group.add(item)

        if curr_group == 2:
            priority += get_priority(group.pop())

        groups[curr_group] = group 
        curr_group = (curr_group + 1) % 3

    return priority


if __name__ == "__main__":
    print(puzzle_one(file_line_generator(__file__)))
    print(puzzle_two(file_line_generator(__file__)))