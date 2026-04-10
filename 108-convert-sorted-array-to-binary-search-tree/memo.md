- Constraints
    - `1 <= nums.length < 10^4`
	- `-10^4 <= nums[i] <= 10^4`
	- `nums` is sorted in a strictly increasing order

## step 1
- 例を見て、Example 1 の解答が なぜ `[0, -3, 5, -10, null, 9]` ではないのか、分からなかったが、高さを揃えるだけではなく、3階層目以降の枝の向きも一致させることを求められている問題だと理解した。
- なるほど、配列は昇順で並んでいるので、根は中央の値にするとして、先に左側の枝を作成して、左側の枝の形に合わせて右の枝も作成するアプローチをとる
- ただし、枝の高さを揃える必要があるので、DFS ではなく、BFS で解くのが良さそう。左から舐めるイメージか
- 木を生成する部分の処理は同じなので、再帰で書けそう

- 時間計算量：`O(n)`
- 空間計算量：`O(n)` ※出力の木も含む場合

```py
from typing import List, Optional


class TreeNode:
	def __init__(self, val=0, left=None, right=None):
		self.val = val
		self.left = left
		self.right = right

class Solution:
	def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
		if not nums:
			return None

		def build_tree(left: int, right: int) -> Optional[TreeNode]:
			if left > right:
				return None

			mid = (left + right) // 2
			root = TreeNode(nums[mid])

			root.left = build(left, mid - 1)
			root.right = build(mid + 1, right)

			return root

		return build(0, len(nums) - 1)
```
- 再帰を使わない version

```py
class Solution:
	def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
		if not nums:
			return None

		mid = (0 + len(nums) - 1) // 2
		root = TreeNode(nums[mid])

		# (node, left_index, right_index)
		stack = [(root, 0, len(nums) - 1)]

		while stack:
			node, left, right = stack.pop()
			mid = (left + right) // 2

			# 左部分木
			if left <= mid - 1:
				left_mid = (left + mid - 1) // 2
				node.left = TreeNode(nums[left_mid])
				stack.append(node.left, left, mid - 1)

			# 右部分木
			if mid + 1 <= right:
				right_mid = (mid + 1 + right) // 2
				node.right = TreeNode(nums[right_mid])
				stack.append((node.right, mid + 1, right))

		return root
```
- 頭の中で考えていた流れに近いが、左部分木なのか、右部分木なのかに関係なく、部分木生成を同じプログラムで処理している1つ目のプログラムの方がスマートである

## step 2
- 他の人の解答を見る

- 参考①：https://github.com/kitano-kazuki/leetcode/pull/24/changes
    - わざわざ `build_tree()` を作らなくても、自分自身の再帰で解ける
	- ただ、外部インターフェースとしてのクラス関数と、ロジックを担うネストファンクションという役割で分けたい場合は、`build_tree()`のような関数を作成して再帰させてもよい

```py
class Solution:
	def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
		if not nums:
			return None
		if len(nums) == 1:
			return TreeNode[nums[0]]

		mid = len(nums) // 2
		root_node = TreeNode(nums[mid])
		left_nums = nums[:mid]
		right_nums = nums[mid + 1:]
		root_node.left = self.sortedArrayToBST(left_nums)
		root_node.right = self.sortedArrayToBST(right_nums)

		return root_node
```
- コメントを読むと、結局 `build_tree()` のような関数を作成して再帰する形に落ち着いていた
- step 1 で記述したパターンとは異なるパターンだが、以下のような書き方もある

```py
class Solution:
	def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
		def sortedArrayToBST_with_range(nums, left, right):
			if left > right:
				return None
			if left == right:
				return TreeNode(nums[left])

			mid = (left + right) // 2
			return TreeNode(
				val=nums[mid],
				left=sortedArrayToBST_with_range(nums, left, mid - 1),
				right=sortedArrayToBST_with_range(nums, mid + 1, right)
			)
		return sortedArrayToBST_with_range(nums, 0, len(nums) - 1)
```
- DFS version
    - ノードの箱を先につくり、中身を後から入れる設計
	- すべてのノードに対して、同じ処理が行われる点がよい

```py
class Solution:
	def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
		root = TreeNode()
		node_to_process = [(0, len(nums) - 1, root)]

		while node_to_process:
				left, right, node = node_to_process.pop()
				mid = (left + right) // 2
				node.val = nums[mid]

				if left <= mid - 1:
					node.left = TreeNode()
					node_to_process.append((left, mid - 1, node.left))
				if mid + 1 <= right:
					node.right = TreeNode()
					node_to_process.append((mid + 1, right, node.right))

		return root
```
- 上記を参考に、step 1 で記述したプログラムを修正してみる

```py
# 再帰

class Solution:
	def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
		if not nums:
			return None

		def build_tree(left: int, right: int) -> Optional[TreeNode]:
			if left > right:
				return None
			if left == right:
				return TreeNode(nums[left])

			mid = (left + right) // 2
			return TreeNode(
				val=nums[mid],
				left=build_tree(left, mid - 1),
				right=build_tree(mid + 1, right)
			)

		return build_tree(0, len(nums) - 1)
```

- 参考③：https://github.com/tom4649/Coding/pull/23/changes
- 再帰の一番シンプルな書き方
    - シンプルではあるものの、プログラムの実行の都度、毎回部分配列をコピーする処理が行われるのは、実務観点ではどうなのだろうか。
	    - LeetCode レベルであれば、どの解法であってもメモリ消費量に大差はない

```py
class Solution:
	def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
		if not nums:
			return None

		mid = len(nums) // 2

		return TreeNode(
			val=nums[mid],
			left=self.sortedArrayToBST(nums[:mid]),
			right=self.sortedArrayToBST(nums[mid + 1:])
		)
```

## step 3
- 時間計算量、空間計算量はいずれのプログラムにおいても同じ
- 個人的に可読性が高く、読んで理解できるプログラムが好きなので、別途、ネストファンクションを作成し、ネストファンクションを再帰で呼び出す解法を最終解とする

```py
class Solution:
	def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
		if not nums:
			return None

		def build_root_within_range(left: int, right: int) -> Optional[TreeNode]:
			if left > right:
				return None

			mid = (left + right) // 2

			return TreeNode(
				val=nums[mid],
				left=build_root_within_range(left, mid - 1),
				right=build_root_within_range(mid + 1, right)
			)

		return build_root_within_range(0, len(nums) - 1)
```
