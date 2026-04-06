- Constraints
    - The number of nodes in the tree is in the range `[1, 50]`.
	- 0 <= Node.val, target <= 1000

## step 1 -> AC
- `root` で与えられる ~~配列~~は、木構造であり、~~配列~~の先頭の値が木の親で、インデックスが大きくなるにつれて、子となる
    -> 配列ではなく、TreeNode 型
- target を境界値として、左の木と右の木に振り分けるところまではイメージがつく
- 左の木の右側の子の値の位置を上位に昇格？してあげるイメージか

- プログラムのイメージが湧かないため、以下を参照
    - https://qiita.com/huront/items/a61fd069b833124e2053
    - https://www.ns.kogakuin.ac.jp/~cu40887/prog4/chapter6.html


```py
from typing import Optional, List


class TreeNode:  # データ型 TreeNode を定義
	def __init__(self, val=0, left=None, right=None):
		self.val = val
		self.left = left
		self.right = right

class Solution:
	def splitBST(self, root: Optional[TreeNode], target: int) -> List[Optional[TreeNode]]:
		if root is None:
			return [None, None]

		if root.val <= target:
			small, large = self.splitBST(root.right, target)
			root.right = small
			return [root, large]
		else:
			small, large = self.splitBST(root.left, target)
			root.left = large
			return [small, root]
```

## step 2
- 他の方の解答も見てみる
- 参考①：https://github.com/potrue/leetcode/pull/47/changes
    - loop でも書けるらしい
	- cpp で書かれているものの、できる限り忠実に python で再現してみる

```py
class TreeNode:
	def __init__(self, val=0, left=None, right=None):
		self.val = val
		self.left = left
		self.right= right

class Solution:
	def splitBST(self, root: Optional[TreeNode], target: int) -> List[Optional[TreeNode]]:
		small = None
		large = None

		small_root = None
		large_root = None

		node = root

		while node:
			if node.val <= target:
				tmp = node.right
				node.right = None

				if small is None:
					small = node
				else:
					small_root.right = node

				small_root = node
				node = tmp
			else:
				tmp = node.left
				node.left = None

				if large is None:
					large = node
				else:
					large_root.left = node

				large_root = node
				node = tmp

		return [small, large]
```
- 木をすべて走査しない、点においては効率的か
- 初見で理解するには複雑かも (python で書くから複雑になるのか？ cpp だと理解しやすい？)

- 参考②：https://github.com/mamo3gr/arai60/pull/58/changes
    - 上記をより分かりやすく書くと、次のようになる？

```py
from typing import Optional, Tuple


class TreeNode:
	def __init__(self, val=0, left=None, right=None):
		self.val = val
		self.left = left
		self.right = right

class Solution:
	def splitBST(self, root: Optional[TreeNode], target: int) -> Tuple[Optional[TreeNode], Optional[TreeNode]]:
		# dummy node (番兵)
		small_dummy = TreeNode(val=-1)
		large_dummy = TreeNode(val=-1)

		small = small_dummy
		large = large_dummy
		node = root

		while node:
			if node.val <= target:
				next_node = node.right
				node.right = None

				small.right = node
				small = node
			else:
				next_node = node.left
				node.left = None

				large.left = node
				large = node

			node = next_node

		return small_dummy.right, large_dummy.left
```
- helper 関数を用いて解く解法もある

```py
class Solution:
	def splitBST(self, root: Optional[TreeNode], target: int) -> Tuple[Optional[TreeNode], Optional[TreeNode]]:
		def helper(node: Optional[TreeNode]) -> Tuple[Optional[TreeNode], Optional[TreeNode]]:
			if node is None:
				return None, None

			if node.val <= target:
				child_left, child_right = helper(node.right)
				node.right = child_left
				return node, child_right
			else:
				child_left, child_right = helper(node.left)
				node.left = child_right
				return child_left, node

		return helper(root)
```
- メモ
    - `Optional[TreeNode]` は、`Union[T, None]` のエイリアスであり、`TreeNode | None` と同じ
	- したがって、`def helper(node: TreeNode | None)` とも書ける
	- 時間計算量は `O(H)` ここで、`H` は木の高さ
	    - 平衡BSTなら `O(log n)`, 偏ったBSTなら `O(N)`
		- python には平衡BSTのメソッドがないため、自作する必要がある。今回は平衡BSTを学ぶことが目的ではないため、一旦スルーする
	- 空間計算量は `O(H)` 再帰スタック分

## step 3
- プログラムの拡張性や、責務分離の観点から、helper 関数を使った解法を解答とする

```py
from typing import Optional, Tuple


class TreeNode:
	def __init__(self, val=0, left=None, right=None):
		self.val = val
		self.left = None
		self.right = None

class Solution:
	def splitBST(self, root: Optional[TreeNode], target: int) -> Tuple[Optional[TreeNode], Optional[TreeNode]]:
		def helper(node: Optional[TreeNode]) -> Tuple[Optional[TreeNode], Optional[TreeNode]]:
			if node is None:
				return None, None

			if node.val <= target:
				small, large = helper(node.right)
				node.right = small
				return node, large
			else:
				small, large = helper(node.left)
				node.left = large
				return small, node

		return helper(root)
```
