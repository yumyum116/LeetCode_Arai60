from collections import deque
from typing import Optional


class Solution:
	def maxDepth(self, root: Optional[TreeNode]) -> int:
		if root is None:
			return 0

		depth = 0
		stack = deque([root])

		while stack:
			count_node = len(stack)

			for _ in range(count_node):
				node = stack.popleft()

				if node.left:
					stack.append(node.left)
				if node.right:
					stack.append(node.right)

			depth += 1

		return depth
