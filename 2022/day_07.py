from common import PuzzleRunner, str_to_ints

class Day7(PuzzleRunner):

    def get_example_str(self) -> str:
        return """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

    def puzzle_one(self, data: list[str]) -> int:
        total = 0 
        for line in data: 
            total += sum([i for i in str_to_ints(line) if i < 100_000])

        return total 

    def puzzle_two(self, data: list[str]) -> int:
        return super().puzzle_two(data)

Day7()