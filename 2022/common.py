import os 
from typing import Generator, AnyStr, Optional, Any

import heapq

def file_line_generator(path:str = None) -> Generator[AnyStr, None, None]:
    if path is None:
        path = "input.txt"

    with open(path, 'r') as file:
        for line in file:
            yield line.rstrip("\r\n")

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