# -*- coding: utf-8 -*-
from tools.runner import PuzzleRunner, str_to_ints


class Node:
    def __init__(
        self,
        name,
        *,
        value=None,
        children: dict[str, "Node"] = None,
        parent: "Node" = None,
    ) -> None:
        self.name = name
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
        self.children[name] = Node(
            name=name, value=value, children=children, parent=self
        )

    def has_children(self) -> bool:
        return len(self.children) > 0


def node_iterator(root: Node):
    queue = [root]
    visited = set([])
    while queue:
        node = queue.pop()

        if node not in visited:
            yield node

            queue.extend(node.children.values())


def strip_command(line: str) -> str:
    parts = line.split(" ")
    command = parts[1]
    target = parts[2] if len(parts) == 3 else None

    return command, target


def __str__(self) -> str:
    return f"{self.name}:{self.value}"


def __repr__(self) -> str:
    return str(self)


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

    def populate_nodes(self, data: list[str]) -> Node:
        root = Node("/")
        curr_node = root

        for line in data:
            if line.startswith("$"):
                command, target = strip_command(line)
                if command == "cd" and target == "..":
                    curr_node = curr_node.up()
                elif command == "cd" and target != curr_node.name:
                    curr_node = curr_node.down(target)
            elif line.startswith("dir"):
                _, target = line.split(" ")
                curr_node.add_child(target)
            else:
                size, name = line.split(" ")
                curr_node.add_child(name, value=str_to_ints(size)[0])

        return root

    def puzzle_one(self, data: list[str]) -> int:
        root = self.populate_nodes(data)

        return sum(
            [
                node.sum_values()
                for node in node_iterator(root)
                if node.has_children() and node.sum_values() < 100_000
            ]
        )

    def puzzle_two(self, data: list[str]) -> int:
        root: Node = self.populate_nodes(data)

        total_disk_space = 70000000
        target_disk_space = 30000000
        curr_disk_space = root.sum_values()
        needed_space = target_disk_space - (total_disk_space - curr_disk_space)

        smallest_dir_size = float("inf")

        for node in node_iterator(root):
            node_size = node.sum_values()
            if (
                node.has_children()
                and node_size > needed_space
                and node_size < smallest_dir_size
            ):
                smallest_dir_size = node_size

        return smallest_dir_size


Day7()
