- Constraints:
    - `m == grid.length`
	- `n == grid[i].length`
	- `1 <= m, n <= 50`
	- grid[i][j]` is either `0` or `1`.

## step 1 -> AC
- `200. Number of Islands` の考え方を応用すれば少ない修正で解けるのでは？
- `num_islands` の部分を、面積を求めるロジックに修正すれば解けそう

```py
from typing import Final


WATER: Final = 0
LAND: Final = 1
DIRECTIONS: Final = ((1, 0), (-1, 0), (0, 1), (0, -1))

class Solution:
	def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
		if not grid or not grid[0]:
			return 0

		num_rows = len(grid)
		num_columns = len(grid[0])
		max_area = 0
		visited = set()

		def is_land(row, column) -> bool:
			if not (0 <= row < num_rows and 0 <= column < num_columns):
				return False
			return grid[row][column] == LAND

		def traverse_island(start_row: int, start_column: int) -> None:
			stack = [(start_row, start_column)]
			visited.add((start_row, start_column))
			area = 1

			while stack:
				row, column = stack.pop()

				for dr, dc in DIRECTIONS:
					neighbor_row = row + dr
					neighbor_column = column + dc

					if (neighbor_row, neighbor_column) in visited:
						continue
					if not is_land(neighbor_row, neighbor_column):
						continue

					stack.append((neighbor_row, neighbor_column))
					visited.add((neighbor_row, neighbor_column))
					area += 1

			return area

		for row in range(num_rows):
			for column in range(num_columns):
				if grid[row][column] == WATER:
					continue
				if (row,column) in visited:
					continue

				max_area = max(max_area, traverse_island(row, column))

		return max_area
```

- BFS の解き方で解いてみる

```py
from collections import deque
from typing import Final


WATER: Final = 0
LAND: Final = 1
DIRECTIONS: Final = ((1, 0), (-1, 0), (0, 1), (0, -1))

class Solution:
	def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
		if not grid and not grid[0]:
			return 0

		num_rows = len(grid)
		num_columns = len(grid[0])
		max_area = 0
		visited = set()

		def is_land(row, column) -> bool:
			if not (0 <= row < num_rows and 0 <= column < num_columns):
				return False
			return grid[row][column] == LAND

		def bfs(start_row: int, start_column: int) -> int:
			queue = deque([(start_row, start_column)])
			visited.add((start_row, start_column))
			area = 1

			while queue:
				row, column = queue.popleft()

				for dr, dc in DIRECTIONS:
					neighbor_row = row + dr
					neighbor_column = column + dc

					if (neighbor_row, neighbor_column) in visited:
						continue
					if not is_land(neighbor_row, neighbor_column):
						continue

					queue.append((neighbor_row, neighbor_column))
					visited.add((neighbor_row, neighbor_column))
					area += 1

			return area

		for row in range(num_rows):
			for column in range(num_columns):
				if grid[row][column] == WATER:
					continue
				if (row, column) in visited:
					continue

				max_area = max(max_area, bfs(row, column))

		return max_area
```

## step 2
- 他の人の解法を見てみる

- 参考①：https://github.com/attractal/leetcode/pull/9/changes
    - 解法は同じ。`WATER` や `LAND`, `DIRECTIONS` を定数として定義するか否か、の違いくらい

- 参考②：https://github.com/Shunii85/arai60/pull/18/changes
    - 同じ考え方をしている（Number Of Islands の応用）

## step 3
- 個人的には `DFS` の解答の方が理解しやすいため、`DFS` で解く

```py
from typing import Final


WATER: Final = 0
LAND: Final = 1
DIRECTIONS: Final = ((1, 0), (-1, 0), (0, 1), (0, -1))

class Solution:
	def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
		if not grid or not grid[0]:
			return 0

		num_rows = len(grid)
		num_columns = len(grid[0])
		max_area = 0
		visited = set()

		def is_land(row, column) -> bool:
			if not (0 <= row < num_rows and 0 <= column < num_columns):
				return False
			return grid[row][column] == LAND

		def traverse_island(start_row: int, start_column: int) -> None:
			stack = [(start_row, start_column)]
			visited.add((start_row, start_column))
			area = 1

			while stack:
				row, column = stack.pop()

				for dr, dc in DIRECTIONS:
					neighbor_row = row + dr
					neighbor_column = column + dc

					if (neighbor_row, neighbor_column) in visited:
						continue
					if not is_land(neighbor_row, neighbor_column):
						continue

					stack.append((neighbor_row, neighbor_column))
					visited.add((neighbor_row, neighbor_column))
					area += 1

			return area

		for row in range(num_rows):
			for column in range(num_columns):
				if grid[row][column] == WATER:
					continue
				if (row,column) in visited:
					continue

				max_area = max(max_area, traverse_island(row, column))

		return max_area
```
