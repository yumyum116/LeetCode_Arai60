- Constraints
    - `m == grid.length`
	- `n == grid[i].length`
	- `1 <= m, n <= 300`
	- `grid[i][j] is `0` or `1`

## step 1 -> AC
- `Island` の十分条件を考える -> 条件を列挙する解き方だと、if 文で多量に分岐することになるため、他のアプローチを考える
- `i` を横方向のインデックス、`j` を縦方向のインデックスとする
    - `[i, j] = 1` である時、次のいずれか一つを満たす場合、`Island` である
	    - `[i, j - 1] = 0` かつ、`[i - 1, j] = 0` かつ、`[i + 1, j] = 0` かつ、`[i, j + 1] = 0` である
		- `[i + 1, j] = 0` であり、`[i, j + 1] = 0` である
		- `[i - 1, j] = 0` であり、`[i, j + 1] = 0` である
	- `[i, j] = 0` である時、次のいずれか一つを満たす場合、`Island` である
	    - etc...

- 解法が浮かばないため、解答を先に見る
    - 似たような問題があった https://qiita.com/MelonPanUryuu/items/171e8c1fd657defce1d8

<!-- プログラムのステップ -->
#### 1. 入力の読み取り
        - `m`, `n`  を読み取る
		- 二次元リストを読み取る
#### 2. 探索の準備
        - 幅優先探索（BFS）用の移動方向リストを準備する
		- 島の数をカウントする変数を初期化する
#### 3. BFS で島を探索
        - 各マスを調査し、黒マス(1)なら新しい島を発見したとみなし、BFS を開始する
		- BFS では、発見した黒マスをキューに追加し、そのマスを白マス(0)に書き換えることで訪問済とする
#### 4. 結果の出力
		- 島の数を出力する

```py
class Solution:
	def numIslands(self, grid: List[List[str]]) -> int:
		if not grid or not grid[0]:
			return 0

		move = [[-1, 0], [0, 1], [1, 0], [0, -1]]  # 移動方向（上下左右）
		islands = 0  # 島の数をカウントする変数
		m = len(grid)  # 行数
		n = len(grid[0])  # 列数

		for i in range(m):
			for j in range(n):
				if grid[i][j] == "0":  # 白マスはスキップ
				    continue

				# 新しい島を発見
				islands += 1
				queue = deque([(i, j)])  # BFS のためのキュー
				grid[i][j] = "0"  # 訪問済のマスを白マスに置き換える

				while queue:
					y, x = queue.popleft()

					for dy, dx in move:
						next_y = y + dy
						next_x = x + dx

						# 境界チェック
						if not (0 <= next_y < m and 0 <= next_x < n):
							continue
						if grid[next_y][next_x] == "0":  # 白マスはスキップ
						    continue

						grid[next_y][next_x] = "0"
						queue.append((next_y, next_x))  # 次のマスをキューに追加

		return islands
```

- 時間計算量は `O(m * n)`
- 空間計算量は、最悪 `O(m * n)`

## step 2
- 他の方の解答を見てみる
- 参考①：https://github.com/komdoroid/arai60/pull/14/changes
    - 解法の組み立てはほぼ同じだが、探索方法が DFS
	- 変数名はこちらの方が分かりやすい

<!-- DFS の流れ -->
#### 1. 探索の開始
#### 2. 現在の状態からの遷移先
#### 3. 重複探索確認
#### 4. 探索終了条件確認

```py
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
					x, y = stack.pop()
					for dr, dc in directions:
						neighbor_x = x + dr
						neighbor_y = y + dc

						if not (0 <= neighbor_x < num_rows and 0 <= neighbor_y < num_columns):
							continue
						if (neighbor_x, neighbor_y) in visited:
							continue
						if grid[neighbor_x][neighbor_y] == "0":
							continue

						stack.append((neighbor_x, neighbor_y))
						visited.add((neighbor_x,neighbor_y))

		return num_islands
```
- 条件分岐を関数にまとめる方法もある
- 以下コメントを参考に、関数に切り出してみる
    - > 外側のループではじめの陸地を見つけて、それ以降四方となりの、同じ島の陸地を訪れていくという流れですよね。

```py
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
				traverse_islands(row, column)

		return num_islands
```
- 関数化の観点で、step 1 で記述したプログラムも改善の余地がありそう

```py
from collections import deque


class Solution:
	def numIslands(self, grid: List[List[str]]) -> int:
		if not grid or not grid[0]:
			return 0

		num_rows = len(grid)
		num_columns = len(grid[0])
		directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
		num_islands = 0

		def flood_fill(start_row: int, start_column: int) -> None:
			queue = deque([(start_row, start_column)])
			grid[start_row][start_column] = "0"

			while queue:
				row, column = queue.popleft()

				for dr, dc in directions:
					neighbor_row = row + dr
					neighbor_column = column + dc

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
```

## step 3
- 好みの問題かもしれないが、DFS の解答の方が関数化による責務分離が明確にできており、理解しやすいため、DFS の解答を step 3 における解答とする。

```py
from typing import Final


WATER: Final = "0"
LAND: Final = "1"
DIRECTIONS: Final = ((1, 0), (-1, 0), (0, 1), (0, -1))

class Solution:
	def numIslands(self, grid: List[List[str]]) -> int:
		if not grid or not grid[0]:
			return 0

		num_rows = len(gird)
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

		for row in range(num_rows):
			for column in range(num_columns):
				if grid[row][column] == WATER:
					continue
				if (row, column) in visited:
					continue

				num_islands += 1
				traverse_island(row, column)

		return num_islands
```
