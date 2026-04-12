from typing import Final


WATER: Final = "0"
LAND: Final = "1"
DIRECTIONS: Final = ((1, 0), (-1, 0), (0, 1), (0, -1))

class Solution:
	def numIslands(self, grid: List[List[str]]) -> int:
		if not grid or not grid[0]:
			return 0

		num_rows = len(grid)
		num_columns = len(grid[0])
		num_islands = 0
		visited = set()

		def is_land(row, column) -> bool:
			if not (0 <= row < num_rows and 0 <= column < num_columns):
				return False
			return grid[row][column] == LAND

		def traverse_island(start_row: int, start_column: int) -> None:
			stack = [(start_row, start_column)]
			visited.add((start_row, start_column))

			while stack:
				current_row, current_column = stack.pop()

				for dr, dc in DIRECTIONS:
					neighbor_row = current_row + dr
					neighbor_column = current_column + dc

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
