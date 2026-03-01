#######################

	step 1

#######################

方針：
①引数で与えられた文字列から、重複を排除した文字列（配列）を作成し、配列の長さが 0 の場合は、-1 を返す。
②引数で与えられた文字列から hash map を生成する。
③重複を排除した文字列を作成するための空の辞書を作成する。
④Hash map に格納されている文字と、②で作成した配列の要素を一つずつ比較する。
　(i) Hash Map に格納されている文字列と一致する文字列が、②で作成した配列の要素に含まれる場合
	　当該要素を②の配列から取り除く
  (ii) (i) 以外の場合
  　　該当する文字列とインデックスのペアを②の配列の末尾に追加する。
⑤~~④(ii)で要素を追加した後に、②の配列の長さを求め、２以上の場合は１番目の要素のインデックスを戻り値として返す。~~
  ②の配列の先頭の要素の値を返す。

```
class Solution:
	def firstUniqChar(self, s: str) -> int:
		result = {}

		for i, character in enumerate(s):
			if character in result:
				del result[character]
			else:
				result[character] = i
		if result:
			return next(iter(result.values()))
		return -1
```

上記の方針の場合、"aaddba" のような文字列の場合は、４番目の"d", 6番目の"a"が戻り値の配列に格納されてしまい、誤答となる。
例えば、２番目の"a"が出てきたタイミングで回答を格納している配列と Hash Map から"a"を削除する方針も考えられるが、　
python の場合は for文開始時の配列の長さが保持されるため、インデックスエラーが生じることが予見される。

キーを文字、文字の登場回数を値として持つ Hash Map を生成することが想起されるが、その場合、元の文字列のインデックス情報がどのように取り出されるのか
イメージが湧かない。元の文字列の Hash Map を作成し、if in でマッチさせてインデックスを取り出す、というアプローチになるのだろうか。

⇛ python の collections.Counter で文字をキー、回数を値とした辞書が作成できるようなので、collections.Counter を使った解法を試してみる。

```
from collections import Counter

class Solution:
	def firstUniqChar(self, s: str) -> int:
		char_count = Counter(s)

		for i, character in enumerate(s):
			if character in char_count:
				if char_count[character] == 1:
					return i
		return -1
```

上記の解法の場合、時間計算量、空間計算量はともに以下のように求められる。

- 時間計算量
 - s の走査：O(n), n は 's' の長さ
 - map の検索：O(1)
 - map の走査：O(m), m は登場する文字の種類の数であり、n >= m となる
 - したがって、時間計算量は O(n) が支配的であるため、O(n)

- 空間計算量
 - 文字をキー、文字の出現頻度を値とした map : O(1)

＊Collections モジュールを使わなくても解けるか？

#######################

	step 2

#######################

他の人の解法も参考にしてみる
 https://github.com/ksaito0629/leetcode_arai60/pull/14/changes
 https://github.com/ksaito0629/leetcode_arai60/pull/14/changes

次のようにも書ける。

class Solution:
	def firstUniqChar(self, s: str) -> int:
		character_to_idx = {}
		seen = set()

		for i, character in enumerate(s):
			if character in seen:
				character_to_idx.pop(character, None)
				continue
			character_to_idx[character] = i
			seen.add(character)

		return next(iter(character_to_idx.values()), -1)

OrderedDict を使う解法もあるらしい。試してみる

```
from collections import OrderedDict

class Solution:
	def firstUniqChar(self, s: str) -> int:
		seen = set()
		unique = OrderedDict()

		for i, character in enumerate(s):
			if character in seen:
				unique.pop(character, None)
				continue
			unique[character] = i
			seen.add(character)

		if not unique:
			return -1

		_, first_unique_char_idx = unique.popitem(last=False)  # 先頭要素を取り出す
		return first_unique_char_idx
	```

#######################

	step 3

#######################

時間計算量や空間計算量には大きな差はないものの、OrderedDict を使う場合は、順序保持と最初の要素を取り出す意図をコード上で明示できるため、
今回は OrderedDict を使ってみる。

```
from collections import OrderedDict

class Solution:
	 def firstUniqChar(self, s: str) -> int:
		seen = set()
		unique = OrderedDict() # 順序を保持しながら辞書を作成する

		for i, character in enumerate(s):
			if character in seen:
				unique.pop(character, None) # 辞書に対して pop メソッドを使う場合の書き方。pop(key, default value)
				continue
			unique[character] = i
			seen.add(character)

		if not unique:
			return -1

		_, first_unique_char_idx = unique.popitem(last=False)	# python 3.7 以降は LIFO順序が保証されているため、最初の要素を取り出す場合は last=False で指定する
		return first_unique_char_idx
```

メモ：
_, idx = dict.popitem(key, value)
の返り値は、{key, value} となる。本問題の場合、value のみが必要となるため、key の保存は不要。
'_' と書くと、戻り値のメモリの占用をしないまま廃棄ができるため、関数からの戻り値が複数あり、不要な値が含まれる場合には、不要な値の場所を '_' に置換すればOK

参考：
https://docs.python.org/ja/3/library/stdtypes.html#dict.popitem
https://qiita.com/fu-a-sak/items/6879cb065ad4c5f0b901

'_' の役割について
https://medium.com/lsc-psd/pythonic%E8%89%B2%E3%80%85-python%E3%81%AE%E3%82%A2%E3%83%B3%E3%83%80%E3%83%BC%E3%82%B9%E3%82%B3%E3%82%A2-%E3%82%92%E4%BD%BF%E3%81%84%E3%81%93%E3%81%AA%E3%81%9D%E3%81%86-3c132842eeef
