- Constraints
    - The number of nodes in the tree is in the range `[1, 50]`.
	- 0 <= Node.val, target <= 1000

## step 1
- `root` で与えられる ~~配列~~は、木構造であり、~~配列~~の先頭の値が木の親で、インデックスが大きくなるにつれて、子となる
    -> 配列ではなく、TreeNode 型
- target を境界値として、左の木と右の木に振り分けるところまではイメージがつく
- 左の木の右側の子の値の位置を上位に昇格？してあげるイメージか

- プログラムのイメージが湧かないため、以下を参照
    - https://qiita.com/huront/items/a61fd069b833124e2053
    - https://www.ns.kogakuin.ac.jp/~cu40887/prog4/chapter6.html


```py
from typing import Optional, List


class TreeNode:
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
