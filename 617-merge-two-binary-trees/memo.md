- Constraints
    - The number of nodes in both trees is in the range `[0, 2000]`
	- `-10^4 <= Node.val <= 10^4`
- Rules
    - ２つのノードがオーバーラップする場合は、各ノードの値を加算し、加算した値を持つノードを新規作成する
	- そうでない場合であって、かつ、ノードが `null` でない場合は、統合前のノードの値を継承する

## step 1 -> AC
- 繰り返し処理で `node.val` を足し合わせるイメージか
    - tree を作成する処理の時間計算量は `O(min(n, m))`
	- 空間計算量は `O(min(n, m))`
	    - `n` は root1 のノード数、`m` は root2 のノード数

```py
from collections import deque
from typing import Optional


class Solution:
	@staticmethod
	def attach_child(
		parent: TreeNode,
		child_name: str,
		child1: Optional[TreeNode],
		child2: Optional[TreeNode],
		queue: deque,
	) -> None:
		if child1 is not None and child2 is not None:
			merged_child = TreeNode(child1.val + child2.val)
			setattr(parent, child_name, merged_child)
			queue.append((merged_child, child1, child2))
		elif child1 is not None:
			setattr(parent, child_name, child1)
		elif child2 is not None:
			setattr(parent, child_name, child2)

	def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
		if root1 is None:
			return root2
		if root2 is None:
			return root1

		merged_root = TreeNode(root1.val + root2.val)
		queue = deque([(merged_root, root1, root2)])

		while queue:
			merged_node, node1, node2 = queue.popleft()

			self.attach_child(merged_node, "left", node1.left, node2.left, queue)
			self.attach_child(merged_node, "right", node1.right, node2.right, queue)

		return merged_root
```
- 何となく、もう少しコンパクトに書ける気がする。気がするが、どこをどう直すとコンパクトになるのか、のイメージは湧かない

## step 2
- 他の人の解法を見る

- 参考①：https://github.com/Shunii85/arai60/pull/23/changes
    - 再帰を使う解き方だとプログラムがシンプルになる。ただ、処理は重め

```py
from typing import Optional
from copy import deepcopy


class Solution:
	def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:

		def mergeTrees_helper(node1: Optional[TreeNode], node2: Optional[TreeNode]) -> Optional[TreeNode]:
			if node1 is None:
				return deepcopy(node2)
			if node2 is None:
				return deepcopy(node1)

			merged_node = TreeNode(val=node1.val + node2.val)
			merged_tree_left = mergeTrees_helper(node1.left, node2.left)
			merged_tree_right = mergeTrees_helper(node1.right, node2.right)
			merged_node.left = merged_tree_left
			merged_node.right = merged_tree_right
			return merged_node

		return mergeTrees_helper(root1, root2)
```

- 参考②：https://github.com/mamo3gr/arai60/pull/22/changes#diff-8ea78d6bde153e5b81489d34a856baeba64b98a9edd82c06d6110c89ba508c5e
    - プログラムが美しい
    - ただし、関数呼び出しの分の時間がかかる

```py
class Solution:
	@staticmethod
	def get_val_left_right_safely(
        node: Optional[TreeNode]
    ) -> Tuple([int, Optional[TreeNode], Optional[TreeNode]]):
		if node is None:
			return 0, None, None
		return node.val, node.left, node.right

	def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
		if root1 is None and root2 is None:
			return None

		val1, left1, right1 = self.get_val_left_right_safely(root1)
		val2, left2, right2 = self.get_val_left_right_safely(root2)

		return TreeNode(
			val=val1 + val2,
			left=self.mergeTrees(left1, left2),
			right=self.mergeTrees(right1, right2)
		)
```

    - こちらの実装も簡潔でよい

```py
class Solution:
	def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
		if root1 is None and root2 is None:
			return None

		if root1 is not None and root2 is None:
			return copy.deepcopy(root1)

		if root1 is None and root2 is not None:
			return copy.deepcopy(root2)

		return TreeNode(
			val=root1.val + root2.val,
			left=self.mergeTrees(root1.left, root2.left),
			right=self.mergeTrees(root1.right, root2.right)
		)
```

- 参考②：https://github.com/Shoichifunyu/shofun/pull/17/changes#diff-954aa7c5bc4f4e1d94e8daf7975f4488a0baa3e27b62659bc873c9d114cd4520R156-R165
    - レビュー後の再リファクタのプログラムが参考になる。ふむ、分岐を減らせるのか

```py
class Solution:
	def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
		def merge_nodes(node1: Optional[TreeNode], node2: Optional[TreeNode]) -> Optional[TreeNode]:
			if node1 is None and node2 is None:
				return None
			if node1 is None:
				node1, node2 = node2, node1

			merged_node = TreeNode(val=node1.val)
			if node2 is None:
				merged_node.left = merge_nodes(node1.left, None)
				merged_node.right = merge_nodes(node1.right, None)
			else:
				merged_node.val += node2.val
				merged_node.left = merge_nodes(node1.left, node2.left)
				merged_node.right = merge_nodes(node1.right, node2.right)

			return merged_node

		return merge_nodes(root1, root2)
```
    - プログラムが破壊的かどうか、という点は今後も気にするべき観点である（そもそも、そのような観点があることを知らなかった）
    - https://docs.google.com/document/d/11HV35ADPo9QxJOpJQ24FcZvtvioli770WWdZZDaLOfg/edit?tab=t.0

- 参考③：https://github.com/tarinaihitori/leetcode/pull/23/changes/BASE..3661cef8b334d992a50e919393c5db1b8e22f9e0#diff-1ede2b2a752e6743ca4d35b115594d80caecd186a464943ab76618d8d1811252
    - 2nd で書かれているようなアプローチは取りたくない（LeetCode で Accept されることが目的であるならば問わないが、
	　実務で使うには危険すぎる）な、と直感的に感じた（プログラムが破壊的であるとはこのことか）
	- 最終解として選んだ再帰のプログラムが分かりやすいか

```py
class Solution:
	def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
		if root1 is None:
			return root2
		if root2 is None:
			return root1

		new_node = TreeNode(root1.val + root2.val)
		new_node.left = self.mergeTrees(root1.left, root2.left)
		new_node.right = self.mergeTrees(root1.right, root2.right)

		return new_node
```

## step 3
- step 2 で学んだ再帰の解き方がシンプルで分かりやすい
- 時間計算量、空間計算量の観点からも過不足ないと判断したため、再帰で解くアプローチを最終解とする

```py
class Solution:
	def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
		if root1 is None:
			return root2
		if root2 is None:
			return root1

		new_node = TreeNode(root1.val + root2.val)
		new_node.left = self.mergeTrees(root1.left, root2.left)
		new_node.right = self.mergeTrees(root1.right, root2.right)

		return new_node
```
- 元の関数の戻り値がヒントになっていた気もする。わざわざ別の関数を作成して、解答を複雑にする必要はなかった
