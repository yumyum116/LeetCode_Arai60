- Constraints:
    - The number of nodes in the tree is in the range `[0, 10^4]`
	- `-100 <= node.val <= 100`

## step 1 -> AC
- 親は必ず2つの子を持つ性質を利用して、配列の先頭の要素から順に探索する
- 木の末端にたどり着いた時の深さを返す
    - 時間計算量：O(n)
	- 空間計算量：O(n)
	- `n` はノードの数

```py
from collections import deque


class TreeNode:
	def __init__(self, val=0, left=None, right=None):
		self.val = val
		self.left = left
		self.right = right

class Solution:
	def maxDepth(self, root: Optional[TreeNode]) -> int:
		if not root:
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
```

## step 2
- 他の人の解答を見る
- 参考①：https://github.com/Shunii85/arai60/pull/21/changes
    - 再帰で解く方法があるらしい

		- 右と左に訪れるのを繰り返す。
		- 手作業的に考えると
		- 今自分はノードの上に立っていて、
		- 自分の次には、右側の人と左側の人がいる。
		- 2人に、立っている場所の深さを教えてあげる。つまり自分の深さ+1
		- どこまで深く行けたのか教えてもらう。
		- 2人のうち大きい方を自分の知っている最大の深さとして、上に報告する。
		- 行き止まりなら、深さを1つ減らして報告する

```py
class Solution:
	def maxDepth(self, root: Optional[TreeNode]) -> int:
		def maxDepthHelper(node: Optional[TreeNode], depth: int) -> int:
			if not node:
				return depth - 1

			left_max_depth = maxDepthHelper(node.left, depth + 1)
			right_max_depth = maxDepthHelper(node.right, depth + 1)
			return max(left_max_depth, right_max_depth)

		return maxDepthHelper(root, 1)
```

- 素直な解法ではあるが、再帰のため実行に時間がかかる。時間計算量は step 1 の解法と同じ

- 参考②：https://github.com/dorxyxki/arai60/pull/21/changes
    - depth も stack で管理する

```py
class Solution:
	def maxDepth(self, root: Optional[TreeNode]) -> int:
		if root is None:
			return 0

		node_and_depth = [(root, 1)]

		def add_child(node: TreeNode, depth: int) -> None:
			if node.left is not None:
				node_and_depth.append((node.left, depth + 1))
			if node.right is not None:
				node_and_depth.append((node.right, depth + 1))

		max_depth = 0

		while node_and_depth:
			node, depth = node_and_depth.pop()
			max_depth = max(depth, max_depth)
			add_child(node, depth)

		return max_depth
```
- よりシンプルな再帰もある

```py
class Solution:
	def maxDepth(self, root: Optional[TreeNode]) -> int:
		if root is None:
			return 0
		return max(self.maxDepth(root.left), self.maxDepth(root.right)) + 1
```
- 問題を高速かつ省メモリで解くという観点では、この解法でいいかもしれない
- 木構造をイメージしながら解く、という観点では、step 1 の解法や、ノードと深さをスタックで管理する解法の方が好ましいか


- 参考③：https://discord.com/channels/1084280443945353267/1227073733844406343/1236695050902048899, その他
- 二分木のノードを順にたどり、行きと帰りのラベルをつけてスタックで管理する解法

```py
class Solution:
	def maxDepth(self, root: Optional[TreeNode]) -> int:
		result_depth_ref = [None]

		# (node, result_depth_ref, left_depth_ref, right_depth_ref)
		stack = [(root, result_depth_ref, [None], [None])]
		while stack:
			node, result_depth_ref, left_depth_ref, right_depth_ref = stack[-1]
			if not node:
				result_depth_ref[0] = 0
				stack.pop()
				continue
			if left_depth_ref[0] is None:
				assert(right_depth_ref[0] is None)
				stack.append((node.left, left_depth_ref, [None], [None]))
				stack.append((node.right, right_depth_ref, [None], [None]))
				continue
			assert(left_depth_ref[0] is not None and right_depth_ref[0] is not None)
			result_depth_ref[0] = max(left_depth_ref[0], right_depth_ref[0]) + 1
			stack.pop()
		return result_depth_ref[0]
```

- 参考④：https://github.com/plushn/SWE-Arai60/pull/21/changes#r2597534088
    > 注意深い読み手はspecial method TreeNode.__bool__()がオーバーライドされてないか気になってしまいます。また実際にTreeNode.__bool__()の実装次第ではnode.leftがNoneでなくとも意図せずimplicit falsyが成立しうる点が危ういと感じるので、個人的にはif node.left is not Noneの方が好ましいと感じます。

	- ふむ。実装によって、必ずしも `if node.left` が `None` ではないのに `False` として扱われる可能性があるということか。
	- この点は自分の step 1 のプログラムにおいても修正すべきところ。`truthiness` を見たいのか、存在チェックをしたいのか
	- while 文の中で for 文を回す実装（step 1）よりも、以下の実装の方がよりシンプルで個人的には好ましいと感じた

```py
class Solution:
	def maxDepth(self, root: Optional[TreeNode]) -> int:
		if root is None:
			return 0

		node_and_level = deque([(root, 1)])
		max_level = 1

		while node_and_level:
			node, level = node_and_level.popleft()

			if node.left is not None:
				node_and_level.append((node.left, level + 1))
			if node.right is not None:
				node_and_level.append((node.right, level + 1))

			max_level = max(max_level, level)

		return max_level
```

## step 3
- step 2 の一番最後の解法を最終解とする

```py
from collections import deque


class TreeNode:
	def __init__(self, val=0, left=None, right=None):
		self.val = val
		self.left = left
		self.right = right

class Solution:
	def maxDepth(self, root: Optional[TreeNode]) -> int:
		if root is None:
			return 0

		node_and_level = deque([(root, 1)])
		max_level = 1

		while node_and_level:
			node, level = node_and_level.popleft()

			if node.left is not None:
				node_and_level.append((node.left, level + 1))
			if node.right is not None:
				node_and_level.append((node.right, level + 1))

			max_level = max(max_level, level)

		return max_level
```
