## step 1

・アプローチ（素案）
	~~①配列の各要素について、昇順にソートした文字列と、要素のインデックス番号を Hash Map に保存する。~~
	~~②①で作成した Hash Map の各文字列について、完全一致する場合には、インデックスを取り出し、元の配列から該当するインデックスの要素を抜き出し、戻り値を格納する配列に追加する。~~
	⇛使用するソート関数にも依存するが、ソート自体の時間計算量が O(nlogn) ~ O(n^2), 各要素の最大長が 100, 配列の長さの最大値が 10^4 であることを考えると、ソートを用いた場合の解法の時間計算量は最大 (10^2)^2*10^4 = 10^8 となる。python が１秒間に処理できる限界が 10^6~10~7 程度の計算量であるため、ソートを用いた場合は、TLEとなる可能性もあることが予想される。したがって、ソートを用いない解法を検討する。

	①配列の各要素ごとに、単語内で登場する文字の種類と数を{'文字の種類':数}として保存する箱を作成する。
	⇛作成されるデータ構造は、str = ["cat", "bat"] という入力値に対して、[[1, [{a:1}, {c:1}, {t:1}]], [2, [{b:1}, {a:1}, {t:1}]]] のような戻り値を返すことをイメージしているが、実現可能か？
	②要素内での{'文字の種類':数}が完全一致する要素を抜き出し、戻り値を格納する配列に追加する。

方針は上記の通りイメージしたものの、実装方法が分からないため、chat-GPT に実現可否も含めて聞いてみた。

回答：実装可能

修正点：
　1. [{a:1}, {c:1}, {t:1}] のような、辞書の配列は比較に手間がかかるため避ける
　⇛ 例えば、"cat" と "tac" を考えた場合に、アルファベットの順番が異なるために、アナグラムであるかどうかの判定が難しくなる。

　　上記の問題を解消する方法として、１単語につき、１つの辞書とする。すなわち、
　　> {'c':1, 'a':1, 't':1}
　　のようにする。
　　
　　文字が出てくる順番が異なる場合においても比較ができるように、タプルに対してソートを行う。
　　> tuple(sorted(count.items()))

実装（例）：

```
from collections import defaultdict


class Solution:
	def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
		groups = defaultdict(list)  # defaultdict は dict-like な辞書を作成するクラス。list を指定することで、key が存在しない時に list() を呼び出して値を作る辞書を作る

		for word in strs:
			count = {}

			for char in word:
				count[char] = count.get(char, 0) + 1  # dict.get(key, default=None) 第二引数は戻り値のデフォルト値を指定する。指定しない場合は None が戻り値

			key = tuple(sorted(count.items()))
			groups[key].append(word)

		return list(groups.values())
```

一応、accept された。が、時間計算量、メモリ使用量ともに改善の余地はありそう。
タプルをソートする処理から、ソートをなくし、ソート無しで同じ結果を得られる処理ができるのか？

## step 2
### 他の人のコードを読む
参考１：https://github.com/tNita/arai60/pull/12/changes
- 文字列をソートするアプローチを採用している
- 各要素の文字列について、ソートした文字列をキー、元の文字列を値とした辞書を作成
- キー値が同じものの値を、defaultdict(list) に追加し、リストとして出力する

```python 3
class Solution:
	def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
		groups = defaultdict(list)
		for original_str in strs:
			sorted_str = "".join(sorted(original_str))  # sorted() の戻り値は list型であり、ハッシュ可能ではないため辞書キーとして使用不可。そのため、文字列に変換し hashable なキーを作成する。
			groups[sorted_str].append(original_str)
		return list(groups.values())  # 戻り値は view であり、辞書のキーや値の現在の状態を動的に反映する参照オブジェクト。配列ではない。配列の場合は、手動での再計算が必要
```

+ 繰り返し処理が一度のみのため、実行時間は step 1 のアプローチの 1/2
+ アプローチも直感的で分かりやすい

参考２：https://github.com/kitano-kazuki/leetcode/pull/12/changes
- `Union find` というアプローチを検討している。（知らないため、後ほど調べる）-> 今回の問題には適さない
- 各単語ごとのハッシュ値を計算し、ハッシュ値が同じものを辞書に追加する
- プログラムはハッシュの計算、1文字あたりのハッシュの計算、groupAnagram から成る

```python 3
class Solution:
	def calculate_hash(self, word):

		# calculate value representing (alphabet, count) pair.
		def calculate_value(alphabet, count):
			seven_bit_maximum = 0b1111111
			if count < 0 or count > seven_bit_maximum:
				raise ValueError(f"count: {count} must be zero or positive and less than or equal to {seven_bit_maximum}")

			a_ord = ord("a")  # 文字に対応するユニコードを返す
			z_ord = ord("z")
			alphabet_ord = ord(alphabet)
			if alphabet_ord < a_ord or z_ord < alphabet_ord:
				raise ValueError(f"alphabet: {alphabet} must be small english letter")

			position = alphabet_ord - a_ord
			num_bit_for_each = 7
			return count << position * num_bit_for_each  # count × 2^(position * 7) と同じ計算。`(position * 7)` は起点を`a`としたときに、対象の文字がどの程度`a`からずれた位置にあるのかを、2進数で計算している

		chr_to_count = {}
		for chr in word:
			chr_to_count.setdefault(chr, 0)
			chr_to_count[chr] += 1

		hash = 0
		for chr, count in chr_to_count.items():
			hash += calculate_value(chr, count)

		return hash


	def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
		hash_to_group = {}
		for word in strs:
			hash_value = self.calculate_hash(word)
			hash_to_group.setdefault(hash_value, [])
			hash_to_group[hash_value].append(word)
		return list(hash_to_group.values())
```

+ 自分でゼロから同じものを書けるか、と言われると、暗記ベースになってしまう。概念は理解できるが、概念をどのようにコードに落とし込めばよいのか、が分からない
+ 計算に時間がかかるようだが、メモリ使用量の観点では、自分の回答と、上に記述した回答よりも改善されている
-> 計算に時間がかかるのは、組み込み関数ではなく、自前の関数でハッシュの計算を行ったから？ネストが深いわけでもないが、for文を2回回している点が、計算に時間がかかった原因か？

## step3
```
配列の各要素をソートして、ソートした文字列をキー、元の文字列を値としてもつ辞書を作成して解く方法が一般的であるようなので、
その解法を本問題における解法とする
```

class Solution:
	def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
		group_anagrams = defaultdict(list)

		for word in strs:
			sorted_word = "".join(sorted(word))
			group_anagrams[sorted_word].append(word)

		return list(group_anagrams.values())

- 時間計算量: O(N*M*logM)
- 空間計算量: O(N*K)

## 感想など
```
引数で与えられた配列の要素の文字列をソートし、ソートした文字列をキー、元の文字列を値に持つ辞書を作成して解く解法であれば、
理解ができればあまり難しくない。

ただし、他の方が書かれているような、自分でハッシュを計算する関数を作成したり、
文字の出現回数のヒストグラムを作成して解く解法は、自分にはまだ難しい。
とくに、ビット演算を用いた解法は非常に苦手。
```
