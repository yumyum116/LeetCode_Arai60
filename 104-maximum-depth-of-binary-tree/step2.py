# recursion ver.1

class Solution:
	def maxDepth(self, root: Optional[TreeNode]) -> int:
		def maxDepthHelper(node: Optional[TreeNode, depth: root]) -> int:
			if not node:
				return depth - 1

			left_max_depth = maxDepthHelper(node.left, depth + 1)
			right_max_depth = maxDepthHelper(node.right, depth + 1)

			return max(left_max_depth, right_max_depth)

		return maxDepthHelper(root, 1)

# recursion ver.2
class Solution:
	def maxDepth(self, root: Optinal[TreeNode]) -> int:
		if root is None:
			return 0
		return max(self.maxDepth(root.left), self.maxDepth(root.right)) + 1

"""
  メモ
  - BFS は heap memory にて明示的に状態を管理する
  - 再帰は、call stack にて暗黙的に状態を管理し、戻り値として返す
"""

# manage depth in stack
class Solution:
	def maxDepth(self, root: Optional[TreeNode]) -> int:
		if root is None:
			return 0

		node_and_depth = [(root, 1)]

		def add_child(node: TreeNode, depth: int) -> None:
			if node.left is not Node:
				node_and_depth.append((node.left, depth + 1))
			if node.right is not Node:
				node_and_depth.append((node.right, depth + 1))

		max_depth = 0

		while node_and_depth:
			node, depth = node_and_depth.popleft()
			max_depth = max(depth, max_depth)
			add_child(node, depth)

		return max_depth

# binary tree
class Solution:
	def maxDepth(self, root: Optional[TreeNode]) -> int:
		result = [None]

		# (node, result, left_depth, right_depth)
		stack = [(root, result, [None], [None])]
		while stack:
			node, result, left_depth, right_depth = stack[-1]
			if not node:
				result[0] = 0
				stack.pop()
				continue
			if left_depth[0] is None:
				assert (right_depth[0] is None)
				stack.append((node.left, left_depth, [None], [None]))
				stack.append((node.right, right_depth, [None], [None]))
				continue
			assert(left_depth[0] is not None and right_depth is not None)
			result_depth[0] = max(left_depth[0], right_depth[0]) + 1
			stack.pop()

		return result[0]

"""
  メモ
  - 再帰を使えない（スタック制限）、あるいは再帰の内部動作を理解するために利用する
"""
