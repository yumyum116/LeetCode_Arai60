- Constraints
    - -100.0 < x < 100.0
	- -2^31 <= n <= 2^31 - 1
	- `n` は整数値
	- `x` は０ではない、または `n > 0` が成り立つ
	- -10^4 <= x^n <= 10^4

## step 1
- 気をつけること：小数点以下も考慮する float or double?
- python の場合、累乗は `**` で表される
- ただし、単に累乗の計算を実行すると、時間計算量は `O(n)` となる。より最適化できないか？

- 以下プログラムは `TLE` となる。

```py
class Solution:
	def myPow(self, x: float, n: int) -> float:
		if x == 0.0:
			return 0.0

		if n == 0:
			return 1.0

		exponent_value = 1.0
		power = abs(n)

		while power > 0:
			exponent_value *= x
			power -= 1

		if n < 0:
			return 1 / exponent_value

		return exponent_value
```

- 時間計算量を `O(log n)` に削減する計算方法として、二分累乗法 `binary exponetiation` という計算方法があるらしい
- 指数 `n` を２の累乗に分解する方法らしいが、そのような組み合わせをどのように見つけるべき？
- 次のような解法があるらしい（参考：https://kazu-yamamoto.hatenablog.jp/entry/20090223/1235372875）
    - `n` が偶数のときは、`x` を二乗し、`n` を半分にする
	- `n` が奇数のときは、結果に `x` を掛け、`x`　はそのまま、`n` を一つ減らす

```py
class Solution:
	def myPow(self, x: float, n: int) -> float:
		if n == 0:
			return 1.0
		if n < 0:
			return 1 / self.myPow(x, -n)
		if n % 2 == 0:
			return self.myPow(x * x, n // 2)
		else:
			return x * self.myPow(x, n - 1)
```

## step 2
- 他の人の解答も参照してみる
- 参考①：https://github.com/5103246/LeetCode_Arai60/pull/43/changes
    - シフト演算を意味する書き方があるらしい
        -https://github.com/Ryotaro25/leetcode_first60/pull/76
	-> ただし、シフト演算は整数に対してのみ使用できる。`float` の場合は使用不可。

- 参考②：https://github.com/mamo3gr/arai60/pull/43/changes#diff-8e640efdb5aaf1ea6722ef8c1369705e0baed0d605aafed97bc3083956cb297aR31-R42
    - ビット演算ができる模様。これは、整数値をとる `n` に対してビット演算を実行しているため可能である。

```py
class Solution:
	def myPow(self, x: float, n: int) -> float:  # right to left binary exponentation
		if n == 0:
			return 1.0
		if n < 0:
			x = 1 / x
			n = -n

		powered = 1
		cumulated_product = x

		while n > 0:
			if n % 2 == 1:  # 最下位ビットが 1 かどうか（奇数か否か）判定
				powered *= cumulated_product
			cumulated_product *= cumulated_product
			n >>= 1  # 次のビットを見る

		return powered

	def myPowLeftToRightBinaryExponentation(self, x: float, n: int) -> float:  # left to right binary exponentation
	    if n < 0:
			x = 1 / x
			n = -n

		powered = 1

		for bit_i in reversed(range(n.bit_length())):  # `n.bit_length()` は、`n` を表すのに必要なビット数。`reversed()` で上位ビットから順に見る
			powered = powered * powered
			if (n >> bit_i) & 1 == 1:  # `n` の `bit_i` 番目のビットを取り出し、そのビットが `1` かどうかを判定
				powered = x * powered

		return powered
```

- 演算部のみインスタンス関数として分ける考え方もある

```py
class Solution:
	def myPow(self, x: float, n: int) -> float:
		if x == 0:
			return 0.0
		if n == 0:
			return 1.0

		negative = n < 0
		if negative:
			n *= -1

		power = self._calculation(x, n)

		if negative:
			return 1 / power
		else:
			return power

	def _calculation(self, x: float, n: int) -> float:
		if n == 0:
			return 1.0

		half = self._calculation(x, n // 2)
		if n % 2 == 0:
			return half * half
		else:
			return half * half * x
```

## step 3
- 時間計算量の観点からは、冒頭の解答を除いて大差ないが、ビット演算の考え方に慣れるため、ビット演算を用いた解答を正とする

```py
class Solution:
	def myPow(self, x: float, n: int) -> float:
		if x == 0.0:
			return 0.0
		if n == 0:
			return 1.0

		if n < 0:
			x = 1 / x
			n = -n

		result = 1.0
		base = x

		while n > 0:
			if n & 1:
				result *= base
			base *= base
			n >>= 1

		return result
```
