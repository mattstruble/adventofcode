from common import PuzzleRunner, str_to_ints

class Node: 
    def __init__(self, value=None, children:dict[str, "Node"]=None, parent:"Node"=None) -> None:
        self.parent = parent 
        self.children = children if children else {}
        self.value = value 

    def sum_values(self) -> int:
        if self.value:
            return self.value 

        return sum([child.sum_values() for child in self.children.values()])
        
    def up(self) -> "Node":
        return self.parent

    def down(self, name) -> "Node":
        return self.children[name]

    def add_child(self, name, value=None, children=None): 
        self.children[name] = Node(value=value, children=children, parent=self)

def node_iterator(root:Node):
    queue = [root]
    visited = set([])
    while queue: 
        node = queue.pop()

        if node not in visited:
            yield node 

            queue.extend(node.children.values())


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