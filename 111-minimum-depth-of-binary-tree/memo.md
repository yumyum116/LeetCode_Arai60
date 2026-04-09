- Constraints
    - The number of nodes in the tree is in the range `[0, 10^5]`
	- `-1000 <= Node.val <= 1000`

## step 1
- 見ているノードが `leaf_node` であるかどうかを判定する必要がある
    - `node.left == None` かつ `node.right == None` であれば、`current_node` は `leaf_node` である
- 見ているノードの階層を `level` で管理して、`min_level = min(min_level, level)` で返すイメージか
    - いや、一番最初に見つかった `leaf_node` のレベルを返せばよいので、`min_level` は不要。
- ~~104. Maximum Depth pf Binary Tree の最小値を返す version~~

```py
from collections import deque


class TreeNode:
	def __init__(self, val=0, left=None, right=None):
		self.val = val
		self.left = left
		self.right = right

class Solution:
	def minDepth(self, root: Optional[TreeNode]) -> int:
		if root is None:
			return 0

		node_and_level = deque([(root, 1)])

		while node_and_level:
			node, level = node_and_level.popleft()

			if node.left is None and node.right is None:
				return level

			if node.left is not None:
				node_and_level.append((node.left, level + 1))
			if node.right is not None:
				node_and_level.append((node.right, level + 1))

		return 0
```

- DFS を再帰で書くなら
    - > recursionlimit(default 1000回)に引っかかるリスクがある(https://github.com/Hiroto-Iizuka/coding_practice/pull/22/changes)

	- このリスクがあるなら、再帰は避けた方が安全か

```py
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
```

- DFS を stack で書く場合

```py
class Solution:
	def minDepth(self, root: Optional[TreeNode]) -> int:
		if root is None:
			return 0

		node_and_level = [(root, 1)]
		min_level = float("inf")  # 深さが正しく評価されないことを防ぐため、正の無限大を初期値として代入

		while node_and_level:
			node, level = node_and_level.pop()

			if node.left is None and node.right is None:
				min_level = min(min_level, level)

			if node.left is not None:
				node_and_level.append((node.left, level + 1))

			if node.right is not None:
				node_and_level.append((node.right, level + 1))

		return min_level
```

## step 2
- 他の人の解法を見る
- https://github.com/Hiroto-Iizuka/coding_practice/pull/22/changes
- https://github.com/naoto-iwase/leetcode/pull/21
    - なるほど、ネストファンクションにはこういう意図もあるのか
	    - https://github.com/naoto-iwase/leetcode/pull/21#discussion_r2430851114
- https://github.com/plushn/SWE-Arai60/pull/22/changes#r2599126066
- https://github.com/Yoshiki-Iwasa/Arai60/pull/25/changes
    - わざわざ left, right を分けずに、`child` として管理する方法もある。python で分かりやすく書き直すとこんな感じか

```py
from collections import deque
from typing import List


class Solution:
	@staticmethod
	def is_leaf(node: TreeNode) -> bool:
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
```
    - わざわざ `node.left`, `node.right` で分けて考える必要がないので、スマートでよいか。
	- `leaf_node` 判定をネストファンクションとして切り出している点も、責務分離の観点でよい


## step 3
- 左右のノードを配列に入れて、ループで回す解き方を最終解とする

```py
from collections import deque
from typing import Optional


class TreeNode:
	def __init__(self, val=0, left=None, right=None):
		self.val = val
		self.left = left
		self.right = right

class Solution:
	@staticmethod
	def is_leaf(node: Optional[TreeNode]) -> bool:
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
```
