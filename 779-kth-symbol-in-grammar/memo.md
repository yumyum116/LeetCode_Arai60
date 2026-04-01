- Constraints
    - 1 <= n <= 30
	- 1 <= k <= 2^{n - 1}

- Rules
    - `n` 行のテーブルを作る
	- 1行目のシンボルは `0` とする
	- ２行目以降では、一つ前の行のシンボルを参照し、以下のルールで置換したものを当該行のシンボルとする
	    - `0` は `01` に置換する
		- `1` は `10` に置換する
	- 関数の引数には、テーブルの行数を表す `n` と、`n` 行目のシンボルの文字の位置を表す `k` が渡される
	- 戻り値として、`n` 行目のシンボルの `k` 番目の文字を返す

## step 1
- 以下条件整理
	- `n >= 3` の場合における、`n` とシンボルの出現パターンを整理する
		- `01` から生み出されるシンボルは `0110`
		- `10` から生み出されるシンボルは `1001`
		- この組み合わせの繰り返し
	- シンボルの文字数の増加パターンを整理する
		- `n = 1` の時、1
		- `n = 2` の時、2
		- `n = 3` の時、4
		- `n = 4` の時、8
		...
		- つまり、シンボルの文字数は `2^{n - 1}` で表される
	- `n`およびシンボルの文字数と `k` との関係を考えてみる
	    - `k = 1, 4, 6, 7,...` の時、シンボルは 0
		- `k = 2, 3, 5, 8,...` の時、シンボルは 1
		- シンボルを１文字ずつ見るよりも、`0110` または `1001` のまとまりで区切って、そのまとまりの中で何番目に位置する文字なのか、を考えた方が解き方としてスマートな気がする
			- `k - 1` を 4 で割った時の商が奇数ならば、`0110`  # `k` が 1 から始まるため、4 で繰り上がるようにインデックスの始まりを 0 に修正
			- `k - 1` を 4 で割った時の商が偶数ならば、`1001`
			- `k` を 4 で割った時の余りがまとまりの中で見たい文字の位置
		- `n` が奇数が偶数か、の場合分けは考えなくて良さそう。あくまで文字数だけ分かれば十分

- 上記で整理した条件を実装に起こしてみる -> 以下のプログラムだと誤答になる

```py
class Solution:
	def kthGrammar(self, n: int, k: int) -> int:
        symbol_length = 2 ** (n - 1)

		if k > symbol_length:
			return -1

		quotient = (k - 1) // 4
		modulo = k % 4

		if quotient % 2 == 0:
			pattern = [0,1,1,0]
			return pattern[modulo - 1]
		else:
			pattern = [1,0,0,1]
			return pattern[modulo - 1]
```
- 上記のアプローチでは解けないようなので、他の方の解答を見てみる
    - 参考①：https://github.com/dxxsxsxkx/leetcode/pull/46/changes#diff-68b94d61743ddc5846f8097490ce0233f6923191ae6b5eb520a8a85400b25a44
	    - 対称性（自分のアプローチの中で "まとまり" と呼んでいるもの）を利用する
		- 一方のまとまりは、他方をフリップしたものであるから、一方の対応する位置のシンボルを2進数の世界の中でフリップしていると考える
		- パターン 1 にあるのか、パターン 2 にあるのかは、演算により求める
		    - 演算式は、シンボルの文字数（長さ） を 2 で割ることにより求められる位置より `k` が大きいか小さいか
			- `k <= pow(2, n - 1) // 2`
			    - `pow()` においては、実行時間が優位なビット演算を使用したい
				    - python の組み込み関数 `pow()` の場合は、型実装に依存する
					- 引数はどちらも `int` 型であり、`int`型の場合は、Cpython においては `longobject.c` の `long_pow` 系の実装が使われる
					    - `long_pow` 系の実装においては、`binary left-to-right algorithm や、指数が大きいときは sliding window を使う` と[公式ドキュメント](https://raw.githubusercontent.com/python/cpython/main/Objects/longobject.c) に記載があるため、組み込み関数の利用で十分に最適化されているものと思慮
					- ちなみに、`float` 型の場合は、`math.pow()` を使用する（`math.pow()` の場合は、`math_pow_impl`が実行される）

```py
class Solution:
	def kthGrammar(self, n: int, k: int) -> int:
		if n == 1 and k == 1:
			return 0

		mid = pow(2, n - 1) // 2

		if k <= mid:
			return self.kthGrammar(n - 1, k)
		else:
			return self.kthGrammar(n - 1, k - mid) ^ 1
```

- なるほど、初期値（0）が固定であるから、条件の真偽の判定で 0 を反転させればよいのか
- まとまりの大きさ 2 の倍数の単位で考えると、後段は前段のシンボルを反転させたものになる
- 後段の場合の初期値は `1` となる

- 最後の、`0`, `1` を反転させる書き方としては、算術演算で書く書き方もある
```py
class Solution:
	def kthGrammar(self, n: int, k: int) -> int:
		if n == 1 and k == 1:
			return 0

		mid = pow(2, n - 1) // 2

		if k <= mid:
			return self.kthGrammar(n - 1, k)
		else:
			return 1 - self.kthGrammar(n - 1, k - mid)
```
- 参考②：https://github.com/olsen-blue/Arai60/pull/47/changes
    - cpp で `return !kthGrammar(n - 1, k - mid)` となっている部分を、ビット演算の `XOR` または算術演算の書き方で書いたが、`int()` で括ってあげる書き方もあるらしい
	    - こちらの書き方の方が直感的で分かりやすいか？

```py
class Solution:
	def kthGrammar(self, n: int, k: int) -> int:
		if n == 1:
			return 0

		if k % 2:
			return int(self.kthGrammar(n - 1, (k + 1) // 2))
		else:
			return int(not self.kthGrammar(n - 1, (k + 1) // 2))
```

> あ、この問題もっとマクロな話をするとビットカウントの偶奇になっていますよ。二分木を考えて、右に行くとビットが反転して、左に行くとしないということですね。
- これを図に表すととても理解しやすい。つまり、`k - 1` を二進数で表すと、ルート(0)からの移動パターンになる。
    - ビット列の場合は `0-indexed` であり、この問題においては `1-indexed` のため、`k - 1` とする
- 移動パターンを二進数で表した場合に、`1` の個数が偶数であれば、`k` 番目のシンボルの値は`0`、奇数であれば `1` になるため、この性質を利用する

```py
class Solution:
	def kthGrammar(self, n: int, k: int) -> int:
		return bin(k - 1).count("1") % 2  # bin() の戻り値は str
```

```py
class Solution:
	def kthGrammar(self, n: int, k: int) -> int:
		return (k - 1).bit_count() % 2
```

## step 2
- 他に解法があるのか、引き続き他の方の解答を参照してみる

- 参考③：https://github.com/mamo3gr/arai60/pull/44/changes#diff-fac6decd64bb207fcf4cb4660ae23dd8b81c5b67788a63e1b6e3371f53371f1e
    - 二分木のイメージを直感的に表現するなら、こう書ける

```py
class Solution:
	def kthGrammar(self, n: int, k: int) -> int:
		if n < 1:
			raise ValueError("n must be grater than 1")
		if n == 1:
			return 0

		parent_n = n - 1
		parent_k = (k + 1) // 2  # 整数の離散性を用いて、`(k + 2 - 1) // 2` とする書き方もあるらしい。（[参考](https://github.com/h1rosaka/arai60/pull/48/changes#r2659245198)）
		parent_symbol = self.kthGrammar(parent_n, parent_k)
		is_left_child = k % 2 == 1

		if parent_symbol == 0:
			if is_left_child:
				return 0
			else:
				return 1
		else:
			if is_left_child:
				return 1
			else:
				return 0
```
- もう少しシンプルに書き直すと、こうなるか

```py
class Solution:
	def kthGrammar(self, n: int, k: int) -> int:
		if n == 1:
			return 0

		parent = self.kthGrammar(n - 1, (k + 1) // 2)

		if k % 2 == 1:
			return parent
		else:
			return 1 - parent
```

- 親子関係を意識するという点においては、上記が分かりやすいか

## step 3
- ３回書いてみる

```py
class Solution:
	def kthGrammar(self, n: int, k:int) -> int:
		if n == 1:
			return 0

		parent = self.kthGrammar(n - 1, (k + 1) // 2)

		if k % 2 == 1:
			return parent
		else:
			return 1 - parent
```


