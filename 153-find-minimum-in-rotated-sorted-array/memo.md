- Constraints
	- time complexity must be within `O(log n)` times.
	- 1 <= n <= 5,000
	- `-5000 <= nums[i] <= 5000`

## step 1 -> fail
- 時間計算量が `O(log n)` 以内に収まることが条件として求められているため、全探索以外の方法で考える必要がある
- i. 	例えば、配列を中央で２つに分割し、前の配列の先頭の要素と後ろの配列の先頭の要素を比較する
- ii. 	後ろの配列の先頭の要素の方が小さい場合は、前の配列の末尾の要素と後ろの配列の先頭の要素を比較する
- iii. 	前の配列の末尾の要素の値の方が小さい場合は、前の配列を中央でさらに２つに分割する
- iv. 	i-iii を繰り返す

- 時間計算量：繰り返し回数が `O(log n)`, 比較回数が毎回 `O(1)` であるから、時間計算量は `O(log n) * O(1) = O(log n)`
- 空間計算量：実装にも依存するが、毎回配列を作らずに添え字を用いるのであれば、`O(1)`

```py -> Wrong Answer
class Solution:
	def findMin(self, nums: list[int]) -> int:
		if len(nums) == 1:
			return nums[0]

		start_former = 0
		end_former = (len(nums) - 1) // 2
		end_latter = len(nums)	 - 1

		for i in range(len(nums)):
			start_latter = end_former + 1
			if nums[start_latter] > nums[start_former]:
				return nums[start_former]
			if nums[start_latter] < nums[start_former] and nums[start_latter] < nums[end_former]:
				return nums[start_latter]
			if nums[start_latter] < nums[start_former] and nums[start_latter] > nums[end_former]:
				end_latter = end_former
				end_former = (end_former - start_former) // 2
				continue
```

### 上記解法のデメリット
- 複数の場合分けを考慮する必要があり、プログラムが複雑になる
- if文の分岐が多く、理解が大変
- index 管理が大変

## step 2
- 他の方の解答を参考にしてみる
- 参考①：https://github.com/dxxsxsxkx/leetcode/pull/42#discussion_r2928098055
	- 配列がソートされていて、かつ、配列の要素が単調増加である性質を利用するとよい
	- step 1 で書こうとしていたのは、この方の `step1_alt.cpp` に書かれているプログラム。python で書き直すと、以下のようになる

```py
class Solution:
	def findMin(self, nums: List[int]) -> int:
		if not nums:
			return -1

		begin = 0
		end = len(nums)
		last = nums[end - 1]

		while begin < end:
			mid = begin + (end - begin) // 2

			if nums[mid] > last:
				begin = mid + 1
			else:
				end = mid

		return nums[begin]
```

> - 配列が単調増加である性質を利用して、各部分配列の要素が単調増加であるのか、そうでないのかを確認する
  - 単調増加ではない部分配列に解答が含まれていることが分かるため、単調増加ではない部分配列を走査対象とする

-> `部分配列が単調増加となる` 性質に気がついていれば、辿り着けた気がする。問題文から、自明の条件を整理した上で、条件をうまく活用して解くアプローチを考えてみるとよいと思った。

- 参考②：https://github.com/tokuhirat/LeetCode/pull/42/changes
- bisect を使う解法がある(https://discordapp.com/channels/1084280443945353267/1230079550923341835/1235694567085576275)

```py
class Solution:
	def findMin(self, nums: List[int]) -> int:
		return nums[bisect_left(nums, True, key=lambda x: x<= nums[-1])]  # x は nums[-1] 以下でなければならない
		return nums[bisect_left(nums, True, key=partial(ge, nums[-1]))]   # `key=partial(ge, nums[-1])` は `key=lambda x: x<= nums[-1]` と同じ
		return nums[bisect_right(nums, False, key=lambda x: x < nums[0]) - len(nums)]  # 負のインデックス -> 配列の最小値を返す
```
- bisect を使う場合の制約：走査する配列はソートされている必要がある
- 直感的な分かりやすさの観点においては、参考①に記載の解答よりも劣後する（自分で書いていても頭の中がこんがらがりそう）


## step 3
- 時間計算量の要件を満たしており、かつ可読性の観点からも以下のコードで過不足ないと判断
- メモリ使用量は改善の余地があるのかもしれないが、可読性と保守性が下がりそうなので、以下を解とする

```py
class Solution:
	def findMin(self, nums: List[int]) -> int:
		if not nums:
			return -1

		left = 0
		right = len(nums)
		last = nums[-1]

		while left < right:
			mid = left + (right - left) // 2

			if nums[mid] > last:
				left = mid + 1
			else:
				right = mid

		return nums[left]
```
