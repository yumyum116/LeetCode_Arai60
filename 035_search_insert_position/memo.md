- Constraints
	- 1 <= nums.length <= 10^4
	- -10^4 <= nums[i] <= 10^4
	- -10^4 <= target <= 10^4

## step 1
- インデックスをキー、要素を値にもつ hash map を作成する
- hash map の値と targaet の値を比較し、一致したらキーを返す
- 比較した値が target より大きい場合は、一つ前のペアの値を返す

```py
class Solution:
	def searchInsert(self, nums: list[int], target: int) -> int:
		num_to_idx = {i: num for i, num in enumerate(nums)}

		for idx, num in num_to_idx.items():
			if num < target:
				continue
			if num >= target:
				return idx
		# hash map の末尾の要素の値が target よりも小さい場合は、キーとなるインデックスに 1 を足した値を返す
		return idx + 1
```

- 時間計算量は O(N) のはずだが、runtime ベースだと、より早い解法があるようだ
- 引数で渡される配列がソートされる性質をうまく利用するべき？ -> 例えば、二分探索の考え方を活用して、配列の中央の要素と target の値を比較する、とか

## step 2
- 他の人の解答を見てみる

### 参考①：https://github.com/dxxsxsxkx/leetcode/pull/41/changes
	- 問題文の条件（制約） をベースに、二分探索の考え方を用いて解いていた
	- cpp で書かれているが、python で書き直してみる。多分こんな感じ

```py
class Solution:
	def searchInsert(self, nums: list[int], target: int) -> int:
		if not nums:  # エッジケース：配列が空の場合（leetCode の問題においては、配列の要素数が１以上という前提が与えられているため、Leetcode の解答としては不要）
			return 0

		begin = 0
		end = len(nums)  # end(right) の初期値がインデックスの範囲外となるため、半閉区間

		while begin < end:
			mid = (begin + end) // 2:  # integer overflow を想定する場合は、 mid = begin + (end - begin) // 2
			if target < nums[mid]:  # 元のコードは '<=' となっているが、ここに等号を含めてしまうと、target = nums[mid] の時の戻り値が想定と異なるのでは？
				end = mid
			else:
				begin = mid + 1
		return begin
```
- 以下コメントが分かりやすい

> ちなみに、私は ng (nums[i] < target) と ok (target <= nums[i]) の境界を求める、と考えるのが一番分かりやすかったです。

```py
class Solution:
	def searchInsert(self, nums: List[int], target: int) -> int:
		ng = -1
		ok = len(nums)

		while (ok - ng > 1):
			mid = (ng + (ok - ng)) // 2
			if nums[mid] >= target:
				ok = mid
			else:
				ng = mid
		return ok
```

###  参考②：https://github.com/potrue/leetcode/pull/41/changes#r2264622846
- 以下問について、自分でも考えてみる
> 1. 区間には何が含まれますか？
	- 解答となり得るインデックス群
> 2. left が指す対象は何ですか？
	- 解答となり得る最小の index（境界を含む）
> 3. right が指す対象は何ですか？
	- 解答となり得る最大の index（境界を含む）
> 4. ループの不変条件 (left < right) を決めるとき、どのように決めましたか？
	-> 条件の意味を深く考えたことがなかった（常識的に考えてそうなる、程度）ため、参考になった
> 5. int mid = (left + right) / 2; のほうがシンプルですが、なぜ int mid = left + (right - left) / 2; なのですか？
	-> LeetCode の問題においては、配列の最大長が 10^4 であるため、オーバーフローの考慮は不要だが、一般的には考えるべき観点として理解した。
	　　いずれにせよ、自分の検討事項からは抜けていた。
> 6. left = mid + 1; の + 1 の部分は、なぜ + 1 なのですか？ - 1 や 0 でないのはなぜですか？
	-> 聞かれると答えられないかも。`mid を計算するときにループが回り続ける可能性がある` について、考えたことがなかった。
> 7. right = mid; にはなぜ - 1 や + 1 を付けていないのですか？
	-> CS における一般的な説明（☓☓を否定しない）と思うが、個人的には分かりにくい。つまり、right には境界を含むため、`-1` をしていない、ということか
> 8. なぜ left を return しているのですか？
	-> 個人的には、left を返す設計としたい。

### 参考③：https://github.com/olsen-blue/Arai60/pull/41/changes
- 再帰で解く解法は浮かばなかったが、個人的には while の方が直感的で分かりやすい

```py
class Solution:
	def searchInsert(self, nums: list[int], target: int) -> int:
		def find_insert_index(left: int, right: int) -> int:
			if left -1 + 1 == right:
				return left
			middle = (left + (right - left)) // 2
			if nums[middle] >= target:
				return find_insert_index(left, middle)
			else:
				return find_insert_index(middle + 1, right)
		return find_insert_index(0, len(nums))
```

## step 3
```py
class Solution:
	def searchInsert(self, nums: List[int], target: int) -> int:
		left = 0
		right = len(nums)

		while left < right:
			mid = left + (right - left) // 2
			if nums[mid] < target:
				left = mid + 1
			else:
				right = mid
		return left
```

### 以下メモ
- 技術面接で聞かれうる内容なんだろうなぁ、と思いながら、いつでも見返せるようにメモ
- 参考：https://discordapp.com/channels/1084280443945353267/1196498607977799853/1269532028819476562　

1. 二分探索を、 [false, false, false, ..., false, true, true, ture, ..., true] と並んだ配列があったとき、 false と true の境界の位置を求める問題、または一番左の true の位置を求める問題と捉えているか？
2. 位置を求めるにあたり、答えが含まれる範囲を狭めていく問題と捉えているか？
3. 範囲を考えるにあたり、閉区間・開区間・半開区間の違いを理解できているか？
4. 用いた区間の種類に対し、適切な初期値を、理由を理解したうえで、設定できるか？
5. 用いた区間の種類に対し、適切なループ不変条件を、理由を理解したうえで、設定できるか？
6. 用いた区間の種類に対し、範囲を狭めるためのロジックを、理由を理解したうえで、適切に記述できるか？

- 本質ではないが、`mid = (left + (right - left)) // 2` とすると、`TLE` になる。なぜ？とりあえず、週末調べる
-> プログラミングの世界では左から順に計算が実行されるのだったか？
