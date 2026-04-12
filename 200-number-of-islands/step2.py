# pattern 1

class Solution:
	def numIslands(self, grid: List[List[str]]) -> int:
		if not grid or not grid[0]:
			return 0

		num_rows = len(grid)
		num_columns = len(grid[0])
		num_islands = 0

		visited = set()
		directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

		for row in range(num_rows):
			for column in range(num_columns):
				if grid[row][column] == "0":
					continue
				if (row, column) in visited:
					continue

				num_islands += 1
				visited.add((row, column))
				stack = [(row, column)]

				while stack:
					current_row, current_column = stack.pop()
					for dr, dc in directions:
						neighbor_y = current_row + dr
						neighbor_x = current_column + dc

						if not (0 <= neighbor_y < num_rows and 0<= neighbor_x < num_columns):
							continue
						if (neighbor_y, neighbor_x) in visited:
							continue
						if grid[neighbor_y][neighbor_x] == "0":
							continue

						stack.append((neighbor_y, neighbor_x))
						visited.add((neighbor_y, neighbor_x))

		return num_islands

# pattern 2

from typing import Final


WATER: Final = "0"
LAND: Final = "1"

class Solution:
	def numIslands(self, grid: List[List[str]]) -> int:
		if not grid or not grid[0]:
			return 0

		num_rows = len(grid)
		num_columns = len(grid[0])
		num_islands = 0
		visited = set()
		directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

		def is_land(row, column) -> bool:
			if not (0 <= row < num_rows and 0 <= column < num_columns):
				return False
			if grid[row][column] == WATER:
				return False
			return grid[row][column] == LAND

		def traverse_island(start_row: int, start_column: int) -> None:
			stack = [(start_row, start_column)]
			visited.add((start_row, start_column))

			while stack:
				row, column = stack.pop()

				for dr, dc in directions:
					neighbor_row = row + dr
					neighbor_column = column + dc

					if (neighbor_row, neighbor_column) in visited:
						continue
					if not is_land(neighbor_row, neighbor_column):
						continue

					stack.append((neighbor_row, neighbor_column))
					visited.add((neighbor_row, neighbor_column))

		for row in range(num_rows):
			for column in range(num_columns):
				if grid[row][column] == WATER:
					continue
				if (row, column) in visited:
					continue

				num_islands += 1
				traverse_island(row, column)

		return num_islands

## step 1 のリファクタリング
from collections import deque


class Solution:
	def numIslands(self, grid: List[List[str]]) -> int:
		if not grid or not grid[0]:
			return 0

		num_rows = len(grid)
		num_columns = len(grid[0])
		directions = ((-1, 0), (1, 0), (0, 1), (0, -1))
		num_islands = 0

		def flood_fill(start_row: int, start_column: int) -> None:
			queue = deque([(start_row, start_column)])
			grid[start_row][start_column] = "0"

			while queue:
				current_row, current_column = queue.popleft()

				for dr, dc in directions:
					neighbor_row = current_row + dr
					neighbor_column = current_column + dc

					if not (0 <= neighbor_row < num_rows and 0 <= neighbor_column < num_columns):
						continue
					if grid[neighbor_row][neighbor_column] == "0":
						continue

					grid[neighbor_row][neighbor_column] = "0"
					queue.append((neighbor_row, neighbor_column))

		for row in range(num_rows):
			for column in range(num_columns):
				if grid[row][column] == "0":
					continue

				num_islands += 1
				flood_fill(row, column)

		return num_islands
