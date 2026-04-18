class Solution:
	def minDepth(self, root: Optional[TreeNode]) -> int:
		if root is None:
			return 0

		def is_leaf(node: Optional[TreeNode]) -> bool:
			if node.left is None and node.right is None:
				return True
			return False

		node_to_level = deque([(root, 1)])

		while node_to_level:
			node, level = node_to_level.popleft()
			if is_leaf(node):
				return level

			if node.left is not None:
				node_to_level.append((node.left, level + 1))
			if node.right is not None:
				node_to_level.append((node.right, level + 1))

		return 0

# recursion ver.
class Solution:
	def minDepth(self, root: Optional[TreeNode]) -> int:
		if root is None:
			return 0

		if root.left is None and root.right is None:
			return 1

		if root.left is None:
			return 1 + self.minDepth(root.right)

		if root.right is None:
			return 1 + self.minDepth(root.left)

		return 1 + min(self.minDepth(root.left), self.minDepth(root.right))

# stack version
class Solution:
	def minDepth(self, root: Optional[TreeNode]) -> int:
		if root is None:
			return 0

		node_and_level = [(root, 1)]
		min_level = float("inf")

		while node_and_level:
			node, level = node_and_level.pop()

			if node.left is None and node.right is None:
				min_level = min(min_level, level)

			if node.left is not None:
				node_and_level.append((node.left, level + 1))

			if node.right is not None:
				node_and_level.append((node.right, level + 1))

		return min_level
