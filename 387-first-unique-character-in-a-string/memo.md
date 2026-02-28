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
⑤④(ii)で要素を追加した後に、②の配列の長さを求め、２以上の場合は１番目の要素のインデックスを戻り値として返す。

class Solution:
	def firstUniqChar(self, s: str) -> int:
		s_deduplication = set(s)
		if not s_deduplication:
			return -1

		result = {}

		for i, character in enumerate(s):
			if character in result:
				del result[character]
			else:
				result[character] = i
			if len(result) >= 2:
				return next(iter(result.values()))
