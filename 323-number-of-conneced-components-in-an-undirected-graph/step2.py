# Union Find
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

# defaultdict
from collections import defaultdict


class Solution:
	def countComponents(self, n: int, edges: List[List[int]]) -> int:
		visited = [False] * n

		def make_adjacent_node_graphs():
			node_to_adjacent_nodes = defaultdict(list)

			for edge in edges:
				node_to_adjacent_nodes[edge[0]].append(edge[1])
				node_to_adjacent_nodes[edge[1]].append(edge[0])
			return node_to_adjacent_nodes

		node_to_adjacent_nodes = make_adjacent_node_graphs()

		def visit_conneced_component(node):
			visited[node] = True
			for next_node in node_to_adjacent_nodes[node]:
				if not visited[next_node]:
					visit_conneced_component(next_node)

		num_connected_components = 0
		for node in range(n):
			if not visited[node]:
				num_connected_components += 1
				visit_conneced_component(node)

		return num_connected_components

# 隣接リストとスタック
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

# 隣接行列と再帰
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
