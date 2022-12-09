from tools.runner import PuzzleRunner
from tools import VDIRS

class Day8(PuzzleRunner):
    
    def get_example_str(self) -> str:
        return """30373
25512
65332
33549
35390"""

    def puzzle_one(self, data: list[str]) -> int:
        grid = []
        for line in data:
            cols = [int(c) for c in line]
            grid.append(cols)

        visible = set([])
        max_cols = [-1] * len(grid[0])
        for r, row in enumerate(grid):
            max_row_val = -1
            for c, tree in enumerate(row):
                if r == 0 or r == len(grid) - 1 or c == 0 or c == len(row) - 1: 
                    visible.add((r,c))
                
                if tree > max_row_val:
                    visible.add((r, c))
                    max_row_val = tree 

                if tree > max_cols[c]:
                    visible.add((r, c))
                    max_cols[c] = tree

        max_cols = [-1] * len(grid[0])
        for r in range(len(grid)-1, -1, -1):
            row = grid[r]
            max_row_val = -1
            for c in range(len(row)-1, -1, -1):
                tree = row[c]
                if r == 0 or r == len(grid) - 1 or c == 0 or c == len(row) - 1: 
                    visible.add((r,c))
                
                if tree > max_row_val:
                    visible.add((r, c))
                    max_row_val = tree 

                if tree > max_cols[c]:
                    visible.add((r, c))
                    max_cols[c] = tree

        return len(visible) 
                

            

    def puzzle_two(self, data: list[str]) -> int:
        grid = []
        for line in data:
            cols = [int(c) for c in line]
            grid.append(cols)

        visible = set([])
        max_cols = [-1] * len(grid[0])
        for r, row in enumerate(grid):
            max_row_val = -1
            for c, tree in enumerate(row):
                if r == 0 or r == len(grid) - 1 or c == 0 or c == len(row) - 1: 
                    visible.add((r,c))
                
                if tree > max_row_val:
                    visible.add((r, c))
                    max_row_val = tree 

                if tree > max_cols[c]:
                    visible.add((r, c))
                    max_cols[c] = tree

        max_cols = [-1] * len(grid[0])
        for r in range(len(grid)-1, -1, -1):
            row = grid[r]
            max_row_val = -1
            for c in range(len(row)-1, -1, -1):
                tree = row[c]
                if r == 0 or r == len(grid) - 1 or c == 0 or c == len(row) - 1: 
                    visible.add((r,c))
                
                if tree > max_row_val:
                    visible.add((r, c))
                    max_row_val = tree 

                if tree > max_cols[c]:
                    visible.add((r, c))
                    max_cols[c] = tree

        max_view = -1 
        for tree in visible: 
            view = 1 
            for dir in VDIRS:
                distance = 0
                x = tree[0]
                y = tree[1]
                while 0 <= x + dir[0] < len(grid) and 0 <= y + dir[1] < len(grid[0]): 
                    distance += 1
                    
                    if grid[x + dir[0]][y + dir[1]] >= grid[tree[0]][tree[1]]:
                        break 

                    x = x + dir[0]
                    y = y + dir[1]


                view *= distance 

            if view > max_view:
                max_view = view

        return max_view

Day8()
