- Constraints
    - `1 <= n <= 2000`
	- `1 <= edges.length <= 5000`
	- `edges[i].length == 2`
	- `0 <= a_i <= b_i < n`
	- `a_i != b_i`
	- There are no repeated edges.

## step 1 -> Failed
- 節点 `k` を訪問済として、深さ優先探索を用いて未訪問の節点を訪問し、隣接リストを作成する
- 隣接リストの長さを返す

```py
class Solution:
	def countComponents(self, n: int, edges: List[List[int]]) -> int:
		if not edges:
			return 0

		adj = {}
		connected = 0

		for i in range(len(edges)):
			for j in range(0, 1):
				if not edge[i][0] in adj:
					adj[edge[i][0]] = [[edge[i][j]]]
					connected += 1
					continue
				if edge[i][j] in adj:
					continue
				if not edge[i][j] in adj:
					adj[edge[i]].append(edges[i][j])

		return len(adj)
```
- このプログラムだと、edge の数をカウントしてしまう

## step 2
- 解き方が分からないので、他の人の解き方を参考にする
    - 参考①：https://github.com/dorxyxki/arai60/pull/19/changes
	    - Union Find で解いていた

```py
class UnionFind:
	def __init__(self, num_nodes: int) -> None:
		self.parent = [i for i in range(num_nodes)]
		self.rank = [1] * num_nodes
		self.num_groups = num_nodes

	def find(self, node: int) -> int:
		if self.parent[node] != node:
			self.parent[node] = self.find(self.parent[node])
		return self.parent[node]

	def union(self, node1: int, node2: int) -> None:
		smaller = self.find(node1)
		bigger = self.find(node2)
		if smaller == bigger:
			return

		if self.rank[smaller] > self.rank[bigger]:
			smaller, bigger = bigger, smaller
		self.parent[smaller] = bigger
		if self.rank[smaller] == self.rank[bigger]:
			self.rank[bigger] += 1
		self.num_groups -= 1

class Solution:
	def countComponents(self, n: int, edges: List[List[int]]) -> int:
		union_find = UnionFind(n)
		for node1, node2 in edges:
			assert node1 != node2
			assert 0 <= node1 < n and 0 <= node2 < n

			union_find.union(node1, node2)

		return union_find.num_groups
```

- 参考②：https://github.com/sakupan102/arai60-practice/pull/22/changes#r1590628823
   - defaultdict を使って解いている
   - 個人的には直感的で分かりやすい
   - プログラムも簡潔でよい

```py
from collection import defaultdict


class Solution:
	def count_components(self, n: int, edges: List[List[int]]) -> int:
		visited = [False] * n

		def make_adjacent_node_graphs():
			node_to_adjacent_nodes = defaultdict(list)

			for edge in edges:
				node_to_adjacent_nodes[edge[0]].append(edge[1])
				node_to_adjacent_nodes[edge[1]].append(edge[0])
			return node_to_adjacent_nodes

		node_to_adjacent_nodes = make_adjacent_node_graph()

		def visit_connected_component(node):
			visited[node] = True
			for next_node in node_to_adjacent_nodes[node]:
				if not visited[nest_node]:
					visit_connected_component(next_node)

		num_connected_components = 0
		for node in range(n):
			if not visited[node]:
				num_connected_components += 1
				visit_connected_component(node)
		return num_connected_components
```
- 隣接リストと stack による探索。
    - Time Complexity: `O(N + E)`
	- Space Complexity: `O(N + E)`

```py
class Solution:
	def countComponents(self, n: int, edges: List[List[int]]) -> int:
		adjacent_nodes = [[] for _ in range(n)]

		for node1, node2 in edges:
			assert 0 <= node1 < n and 0 <= node2 < n
			adjacent_nodes[node1].append(node2)
			adjacent_nodes[node2].append(node1)

		visited = [False] * n

		def visit_connected_nodes(first_node: int) -> int:
			nodes_to_check = [first_node]
			while nodes_to_check:
				node = nodes_to_check.pop()
				if visited[node]:
					continue

				visited[node] = True
				nodes_to_check.extend(adjacent_nodes[node])

		count = 0
		for node_index in range(n):
			if not visited[node_index]:
				visit_connected_nodes(node_index)
				count += 1

		return count
```

- 隣接行列と再帰による探索もある
    - Time Complexity: O(n^2)
	- Space Complexity: O(n^2)

```py
class Solution:
	def countComponents(self, n: int, edges: List[List[int]]) -> int:
		is_connected = [[False] * n for _ in range(n)]

		for node1, node2 in edges:
			assert 0 <= node1 < n and 0 <= node2 < n
			is_connected[node1][node2] = True
			is_connected[node2][node1] = True

		visited = [False] * n

		def traverse(i: int) -> None:
			visited[i] = True
			for j in range(n):
				if is_connected[i][j] and not visited[j]:
					traverse(j)

		num_connected = 0
		for i in range(n):
			if not visited[i]:
				traverse(i)
				num_connected += 1

		return num_connected
```
- プログラムはシンプルでよいが、時間計算量の観点では最適ではない。

## step 3
- 隣接リストと stack により探索するプログラムを、`visited` 済かどうかを、`push`前に判定するプログラムに修正

```py
class Solution:
	def countComponents(self, n: int, edges: List[List[int]]) -> int:
		graph = [[] for _ in range(n)]

		for node1, node2 in edges:
			graph[node1].append(node2)
			graph[node2].append(node1)

		visited = [False] * n
		components = 0

		for start in range(n):
			if visited[start]:
				continue

			components += 1
			stack = [start]
			visited[start] = True

			while stack:
				node = stack.pop()
				for neighbor in graph[node]:
					if not visited[neighbor]:
						visited[neighbor] = True
						stack.append(neighbor)

		return components
```
