from collections import deque
from typing import Optional


class Solution:
    def is_leaf(self, node: Optional[TreeNode]) -> bool:
        return node.left is None and node.right is None

    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        node_and_level = deque([(root, 1)])

        while node_and_level:
            node, level = node_and_level.popleft()

            if self.is_leaf(node):
                return level
            for child in (node.left, node.right):
                if child is not None:
                    node_and_level.append((child, level + 1))

        raise RuntimeError("unreachable")
