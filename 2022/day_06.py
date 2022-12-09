# -*- coding: utf-8 -*-
from tools.runner import PuzzleRunner


class Day6(PuzzleRunner):
    def get_example_str(self) -> str:
        return """mjqjpqmgbljsphdztnvjfqwrcgsmlb
bvwbjplbgvbhsrlpgdmjqwftvncz
nppdvjthqldpwncqszvftbrmjlhg
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"""

    def puzzle_one(self, data: list[str]) -> int:
        seen = set([])
        pos = []
        for line in data:
            for i, c in enumerate(line):
                if c in seen:
                    seen.clear()

                seen.add(c)

                if len(seen) == 4:
                    pos.append(i)
                    break

        return pos

    def puzzle_two(self, data: list[str]) -> int:
        seen = {}
        last_pos = -1
        result = []
        for line in data:
            seen = {}
            last_pos = -1
            for i, c in enumerate(line):
                if c in seen and seen[c] >= last_pos:
                    last_pos = seen[c] + 1

                if i - last_pos >= 13:
                    result.append(i + 1)
                    break

                seen[c] = i

        return result


Day6()
