- Constraints
	- Time complexity : `O(log n)`
	- An array is sorted in ascending order with distinct values
	- Given the array `nums` after the possible rotation and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.

## step 1
- `153. Find Minimum in Rotated Sorted Array` と同様の解法で解く
- `153` の問題で `last = array[-1]` としていたところを `var = target` とすればよい？ -> 今回は、探している値が引数で渡されるため、hash map を作成するか
- 今回のケースは、`target` の値が与えられた配列に含まれる場合は、True / False の境界が２つ以上になり、単調列ではないため、bisect は使えない

### pattern 1
```py
class Solution:
	def search(self, nums: List[int], target: int) -> int:
		left = 0
		right = len(nums) - 1

		while left <= right:
			mid = left + (right - left) // 2

			if nums[mid] == target:
				return mid

			if nums[left] <= nums[mid]:
				if nums[left] <= target < nums[mid]:
					right = mid - 1
				else:
					left = mid + 1

			else:
				if nums[mid] < target <= nums[right]:
					left = mid + 1
				else:
					right = mid - 1

		return -1
```

### pattern 2 : hash map
```py
class Solution:
	def search(self, nums: List[int], target: int) -> int:
		for idx, value in enumerate(nums):
			if value == target:
				return idx
		return -1
```

- pattern 1 でも悪くはないが、条件分岐が複雑、かつ、同じような処理が複数回出てくるのがイケてない
- pattern 2 は実装がシンプルで、時間計算量も平均 `O(1)` に収まる

## step 2
### 他の人の解答を参照してみる
- 参考①：https://github.com/5103246/LeetCode_Arai60/pull/41/changes
	- この質問と回答は自明。step 1 - pattern 1 も改善できる
		https://github.com/5103246/LeetCode_Arai60/pull/41/changes#r2904298564
	- なるほど、関数化すればよいのか -> python で書き直してみる

```py
class Solution:
	def search(self, nums: List[int], target: int) -> int:
		if not nums:
			return -1

		min_index = self.findMin(nums)

		if target <= nums[-1]:
			return self.binarySearch(nums, target, min_index, len(nums))
		else:
			return self.binarySearch(nums, target, 0, min_index)

	def findMin(self, nums: List[int]) -> int:
		left = 0
		right = len(nums)

		while left < right:
			mid = left + (right - left) // 2

			if nums[mid] <= nums[-1]:
				right = mid
			else:
				left = mid + 1

		return left

	def binarySearch(self, nums: List[int], target: int, left: int, right: int) -> int:
		while left < right:
			mid = left + (right - left) // 2

			if nums[mid] >= target:
				right = mid
			else:
				left = mid + 1

		if nums[left] != target:
			return -1

		return left
```

- 時間計算量は `O(log n)` だが、hash map と比較しても十分に早い
- 一方、メモリ使用量は `O(1)` で済むため、この解答が一番望ましいか

- 参考②：https://github.com/naoto-iwase/leetcode/pull/26/changes
	- bisect でも解けるらしい（自分も書いてみたが、断念した）

```py
from typing import List
import bisect


class Solution:
	def search(self, nums: List[int], target: int) -> int:
		min_index = bisect.bisect_left(nums, True, key=lambda x: x <= nums[-1])  # 配列の要素の中で、最小となる要素のインデックスを調べる
		if target <= nums[-1]:
			target_index = bisect.bisect_left(nums[min_index:], target) + min_index  # min_index を起点とした時の相対位置を求めるのか。なるほど
		else:
			target_index = bisect.bisect_left(nums[:min_index], target)
		if nums[target_index] == target:
			return target_index
		return -1
```

- この問題であれば、bisect を使った解法も分かりやすい
- スライスを使用すると、時間計算量、空間計算量ともに `O(n)` になるため、計算量の観点では最適ではない
- 時間計算量：`O(log n)`, 空間計算量 `O(1)` にするのであれば、以下のようになる

```py
from typing import List
import bisect


class Solution:
	def search(self, nums: List[int], target: int) -> int:
		min_index = bisect.bisect_left(nums, True, key=lambda x: x <= nums[-1])

		if target <= nums[-1]:
			lo, hi = min_index, len(nums)
		else:
			lo, hi = 0, min_index

		target_index = bisect.bisect_left(nums, target, lo=lo, hi=hi)

		if target_index < len(nums) and nums[target_index] == target:
			return target_index

		return -1
```
- key 関数をいじる解法もある

```py
from typing import List
import bisect


class Solution:
	def search(self, nums: List[int], target: int) -> int:
		key_function = lambda x: (x <= nums[-1], x)
		index = bisect.bisect_left(nums, key_function(target), key=key_function)

		if index < len(nums) and nums[index] == target:
			return index

		return -1
```
- コードはシンプルでよいが、初見で理解に時間がかかる

## step 3
- 個人的には、目的ごとに関数を作成する解法がよい（作成した関数の再利用も効く）と考えた

```py
class Solution:
	def search(self, nums: list[int], target: int) -> int:
		if not nums:
			return -1

		left = 0
		right = len(nums)
		min_index = self.findMinIndex(nums)

		if target <= nums[-1]:
			left = min_index
		else:
			right = min_index

		return self.findTargetIndex(nums, target, left, right)

	def findMinIndex(self, nums: List[int]) -> int:
		left = 0
		right = len(nums)

		while left < right:
			mid = left + (right - left) // 2

			if nums[mid] <= nums[-1]:
				right = mid
			else:
				left = mid + 1

		return left

	def findTargetIndex(self, nums: List[int], target: int, left: int, right: int) -> int:
		while left < right:
			mid = left + (right - left) // 2

			if nums[mid] >= target:
				right = mid
			else:
				left = mid + 1

		if nums[left] != target:
			return -1

		return left
```
