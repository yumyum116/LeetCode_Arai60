from collections import defaultdict
from typing import List


class Solution:
	def countComponents(self, n: int, edges: List[List[int]]) -> int:
		if not edges:
			return n

		node_to_adjacent_nodes = defaultdict(list)

		for node1, node2 in edges:
			node_to_adjacent_nodes[node1].append(node2)
			node_to_adjacent_nodes[node2].append(node1)

		num_components = 0
		visited = [False] * n

		for node in range(n):
			if visited[node]:
				continue

			num_components += 1
			stack = [node]
			visited[node] = True

			while stack:
				current_node = stack.pop()

				for next_node in node_to_adjacent_nodes[current_node]:
					if visited[next_node]:
						continue

					visited[next_node] = True
					stack.append(next_node)

		return num_components
