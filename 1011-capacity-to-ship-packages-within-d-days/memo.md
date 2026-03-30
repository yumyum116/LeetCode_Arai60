- Constrains
	- 1 <= days <= weights.length <= 5 * 10^4
	- 1 <= weights[i] <= 500

## step 1 -> TLE になる
   - `days` < `max(weights)` であれば、`max(weights)` を仮の解答として以下を実施する
      (i)`weights`の先頭の要素から順に足していき、`max(weights)` を超えない要素の組を、組の数が `days` を超えない範囲で作成する
	  (ii) 組を作成している途中で 組の数が `days` を超えた場合は、`max(weights)` に 1 を加算した値と次の解とする
	  (iii) (i) が正の場合は、`max(weights)` を返す。
	  (iv) (i)-(iii) を繰り返す
   - `days` >= `max(weights)` の場合は、`max(weights)` を仮の解答として以下を実施する
      (i)`weights`の先頭の要素から順に足していき、`max(weights)` を超えない要素の組を、組の数が `days` を超えない範囲で作成する
	  (ii) 組を作成している途中で 組の数が `days` を超えた場合は、`max(weights)` に 1 を減算した値と次の解とする
	  (iii) (i) が正の場合は、`max(weights)` を返す。
	  (iv) (i)-(iii) を繰り返す

```py
class Solution:
	def shipWithinDays(self, weights: List[int], days: int) -> int:
		if not weights:
			return -1

        least_weight = max(weights)

		while True:
			i = 0
			count = 0  # 要素の和が least_weight を超えない組の数をカウントするカウンタ

			while i < len(weights):
				current_sum = 0

				while i < len(weights) and current_sum + weights[i] <= least_weight:
					current_sum += weights[i]
					i += 1

				count += 1

			if count <= days:
				return least_weight

			leaast_weight += 1
```
- 時間計算量が最悪 `O(n^2)` となる。平均時間計算量は `O(n * (S - M + 1))`。ここで、`S` は `sum(weights)（終了値）`, `M` は `max(weights)(開始値)`
- 本問題においては、weights の要素数が最大で `5 * 10^4` となるため、python が１秒間に演算可能な `10^6-10^7` を超過し、`TLE` となる

## step 2
- 他の人の解答を見る
- 参考①：https://github.com/5103246/LeetCode_Arai60/pull/42/changes
    - 自分は問題で与えられた例をベースに、頭に浮かんだ解法で解けるか試してみたが、以下のような思考の深堀が足りていなかった
	> days日全てを使って積んだ方が積める重さも減るので、日数を余らせちゃダメか。

    > - 積載重量の上限（high）はweightsの合計で、下限（low）がmax(weights)
    > - 求める積載重量は、一番小さくてmax(weights)で、1日に全て詰め込むときが最大なのでweightsの合計になる。
    > - middleでdays以内に運べたら、middle ~ lowで探索する。middleでdays以内に運べなかったら、積載重量が足りないので high ~ middle + 1 で探索する。

	- なるほど、解答となり得る重さの下限値と上限値の範囲の中で二分探索をするのか。二分探索の範囲自体を計算で求める発想がなかった
    - 解答はcpp だが、python で書くとおそらくこんな感じだろう

```py
class Solution:
	def shipWithinDays(self, weights: List[int], days: int) -> int:
		if not weights:
			return 0

		low_weight = max(weights)
		high_weight = sum(weights)

		while low_weight < high_weight:
			mid_weight = low_weight + (high_weight - low_weight) // 2
			days_with_capacity = self.calculateDays(weights, mid_weight)

			if days_with_capacity <= days:
				high_weight = mid_weight
			else:
				low_weight = mid_weight + 1

		return low_weight

	def calculateDays(self, weights: List[int], capacity: int) -> int:
		days = 1
		total_weight = 0

		for weight in weights:
			if total_weight + weight > capacity:
				total_weight = 0
				days += 1

			total_weight += weight

		return days
```
- わざわざ calculateDays()でいちいち求めずとも解けないか？
-> かかる日数を返すのではなく、計算結果が `days` 以内に収まるかを調べて、bool値で返す、という考え方がある（なるほど！！）
-> `TLE` になる

```py
class Solution:
	def shipWithinDays(self, weights: List[int], days: int) -> int:
		if not weights:
			return 0

		low_weight = max(weights)
		high_weight = sum(weights)

		while low_weight < high_weight:
			mid_weight = low_weight + (high_weight - low_weight) // 2

			if self.isShippable(weights, mid_weight, days):
				high_weight = mid_weight
			else:
				low_weight = mid_weight + 1

		return low_weight

	def isShippable(self, weights: List[int], capacity: int, days: int) -> bool:
		days_required = 1
		total_weight = 0

		for weight in weights:
			if total_weight + weight > capacity:
				total_weight = 0
				days_required += 1

			total_weight += weight

		return days_required <= days
```

- 参考②：https://github.com/fhiyo/leetcode/pull/45/changes
- bisect_left を使う解き方もあるらしい
- 可読性および単一責任原則の観点から、ネスト関数をインスタンス関数に修正

```py
class Solution:
	def shipWithinDays(self, weights: List[int], days: int) -> int:
		assert days > 0
		if not weights:
			return 0

		return bisect_left(
			range(sum(weights) + 1),
			True,
			key=lambda capacity: self.can_be_shipped(weights, days, capacity)
		)

	def can_be_shipped(self, weights: List[int], days: int, capacity: int) -> bool:
		total_weight = 0
		required_days = 0

		for weight in weights:
			if weight > capacity:
				return False
			if total_weight + weight > capacity:
				total_weight = 0
				required_days += 1
				if required_days > days:
					return False

			total_weight += weight

		return required_days + 1 <= days
```
- 初見だと理解に時間がかかる

## step 3
- 時間計算量、空間計算量の観点では、いずれの解法も大差はない
- よって、可読性の観点から、指定の重さで輸送するためにかかる日数が`days` 以内に収まるかどうかを調べて、bool値で返す解答を final answer とする

```py
class Solution:
	def shipWithinDays(self, weights: List[int], days: int) -> int:
		assert days > 0
		if not weights:
			return 0

		low_weight = max(weights)
		high_weight = sum(weights)

		while low_weight < high_weight:
			mid_weight = low_weight + (high_weight - low_weight) // 2

			if self.can_be_shipped(weights, mid_weight, days):
				high_weight = mid_weight
			else:
				low_weight = mid_weight + 1

		return low_weight

	def can_be_shipped(self, weights: List[int], capacity: int, days: int) -> bool:
		days_required = 1
		total_weight = 0

		for weight in weights:
			if total_weight + weight > capacity:
				total_weight = 0
				days_required += 1

			total_weight += weight

		return days_required <= days
	```
