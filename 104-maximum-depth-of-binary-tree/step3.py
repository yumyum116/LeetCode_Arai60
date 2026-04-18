from collections import deque
from typing import Optional


class Solution:
	def maxDepth(self, root: TreeNode[Optional]) -> int:
		if not root:
			return 0

		frontier = deque((root, 1))
		max_level = 1

		while frontier:
			node, level = frontier.popleft()

			if node.left is not None:
				frontier.append((node.left, level + 1))
			if node.right is not None:
				frontier.append((node.right, level + 1))

			max_level = max(max_level, level)

		return max_level
