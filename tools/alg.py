# -*- coding: utf-8 -*-
import heapq
from typing import Any, Optional


class MinHeap:
    def __init__(self, max_size: Optional[int] = None):
        self.max_size = max_size
        self.heap = []

    def push(self, x: Any):
        if self.max_size and len(self) >= self.max_size:
            heapq.heappushpop(self.heap, x)
        else:
            heapq.heappush(self.heap, x)

    def pop(self):
        return heapq.heappop(self.h)

    def __getitem__(self, i) -> Any:
        return self.heap[i]

    def __len__(self):
        return len(self.heap)

    def __str__(self) -> str:
        return str(self.heap)


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

    def __str__(self) -> str:
        return f"{self.name}:{self.value}"

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def iterator(root: "Node"):
        queue = [root]
        visited = set([])
        while queue:
            node = queue.pop()

            if node not in visited:
                yield node

                queue.extend(node.children.values())
