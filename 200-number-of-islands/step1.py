from collections import deque


class Solution:
	def numIslands(self, grid: List[List[str]]) -> int:
		if not grid or not grid[0]:
			return 0

		move = [(-1, 0), (1, 0), (0, -1), (0, 1)]
		islands = 0
		num_rows = len(grid)
		num_columns = len(grid[0])

		for row in range(num_rows):
			for column in range(num_columns):
				if grid[row][column] == "0":
					continue

				islands += 1
				queue = deque([(row, column)])
				grid[row][column] = "0"

				while queue:
					y, x = queue.popleft()

					for dy, dx in move:
						next_y = y + dy
						next_x = x + dx

						if not (0 <= next_y < num_rows and 0 <= next_x < num_columns):
							continue
						if grid[next_y][next_x] == "0":
							continue

						grid[next_y][next_x] = "0"
						queue.append((next_y, next_x))

		return islands
