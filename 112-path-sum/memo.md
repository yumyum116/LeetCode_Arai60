- Constraints
    - The number of nodes in the tree is in the range `[0, 5000]`
	- `-1000 <= Node.val <= 1000`
	- `-1000 <= targetSum <= 1000`

## step 1
- すべてのパスを確かめる場合、時間計算量は `O(n)`
- 例えば、`足し合わせた結果 = targetSum` よりも、次のノードが `leaf` で、かつ、`leaf` の値が、`targetSum` から一つ前までのノードの合計を引いた残りに一致するかどうかを見るロジックの方がよかったりするか？
    - 単に `leaf` まで足し合わせてその合計値と `targetSum` を比較した方がシンプルでよいかもしれない
	- 到達したノードまでの合計値を保持しておく必要がある -> キューで管理する
- 空間計算量は `O(n)`

```py
class Solution:
	def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
		if not root:
			return False

		queue = ([(root, root.val)])

		while queue:
			node, current_sum = queue.popleft()

			if node.left is None and node.right is None:
				return current_sum == targetSum

			if node.left is not None:
				queue.append((node.left, current_sum + node.left.val))
			if node.right is not None:
				queue.append((node.right, current_sum + node.right.val))
```

## step 2
- 他の人の解法を見る
- 参考①：https://github.com/Shunii85/arai60/pull/25/changes
- DFS で解くパターン。python で書き直してみる

```py
class Solution:
	@staticmethod
	def is_leaf(node: Optional[TreeNode]) -> bool:
		return node.left is None and node.right is None

	def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
		def hasPathSumHelper(
			node: Optional[TreeNode],
			current_sum: int,
			target_sum: int
		) -> bool:
			if not node:
				return False

			current_sum += node.val

			if self.is_leaf(node) and current_sum == targetSum:
				return True

			return (
				hasPathSumHelper(node.left, current_sum, targetSum)
				or hasPathSumHelper(node.right, current_sum, targetSum)
			)

		return hasPathSumHelper(root, 0, targetSum)
```

- 参考②：https://github.com/rossy0213/leetcode/pull/14/changes#diff-34efe727dd1ad18d2b320e1e34b81b9129b8d0af26c5e979c65907a7f3f23d3bR41-R55
    - `targetSum` と `node.val` の差をとって、差と見ているノードの値が等しいかどうかを見るプログラム
	- これでもよい

```py
class Solution:
	@staticmethod
	def _is_leaf(node: Optional[TreeNode]) -> bool:
		return node.left is None and node.right is None

	def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
		if not root:
			return False

		if self._is_leaf(root):
			return root.val == targetSum

		remaining = targetSum - root.val

		return self.hasPathSum(root.left, remaining) or self.hasPathSum(root.right, remaining)
```

- 参考③：https://github.com/tom4649/Coding/pull/24/changes
    - left, right を分けずに、child として扱って、for 文でなめる解き方

```py
class Solution:
	@staticmethod
	def _is_leaf(node: Optional[TreeNode]) -> bool:
		return node.left is None and node.right is None

	def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
		if root is None:
			return False

		node_to_process = deque()
		node_to_process.append((root, 0))

		while node_to_process:
			node, current_sum = node_to_process.pop()

			if node is None:
				continue
			current_sum += node.val

			if self._is_leaf(node) and current_sum == targetSum:
				return True
			for child in [node.left, node.right]:
				node_to_proceed.append((child, current_sum))

		return False
```
- 参考④：https://github.com/PafsCocotte/leetcode/pull/7/changes
- よりシンプルに書くなら、こういう書き方もある

```py
class Solution:
	@staticmethod
	def _is_leaf(node: Optional[TreeNode]) -> bool:
		return node.left is None and node.right is None

	def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
		if root is None:
			return False

		targetSum -= root.val

		if self._is_leaf(root):
			return targetSum == 0

		return self.hasPathSum(root.left, targetSum) or self.hasPathSum(root.right, targetSum)
```
- targetSum は上書かない方が望ましいか

## step 3
- どの解法でも大差はないが、`remaining` を使う解法を最終解とする

```py
class Solution:
	@staticmethod
	def _is_leaf(node: Optional[TreeNode]) -> bool:
		return node.left is None and node.right is None

	def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
		if root is None:
			return False

		remaining_sum = targetSum - root.val

		if self._is_leaf(root):
			return root.val == targetSum

		return self.hasPathSum(root.left, remaining_sum) or self.hasPathSum(root.right, remaining_sum)
```
