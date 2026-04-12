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
