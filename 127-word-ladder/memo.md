- Constraints
    - `1 <= beginWord.length <= 10`
	- `endWord.length == beginWord.length`
	- `1 <= wordList.length <= 5000`
	- `wordList[i].length == beginWord.length`
	- `beginWord, endWord, and wordList[i] consist of lowercase English letters.`
	- `beginWord != endWord`
	- `All the words in wordList are unique.`

## step 1 -> WA
- アプローチ
    - 配列の要素を隣同士で比較する
	- 要素は list に1文字ずつ格納し、list の長さが同じであれば、以下を行う
	    - 一致する文字の数が `len(list) - 1` の場合、`transformation` であると判定する
		- `transformation` であると判定された単語を stack に追加する
	- stack の長さを返す
	- 以下の条件のいずれかに合致する場合は、比較対象外とする
	    - `wordList[-1] != endWord`
		- `len(list1) != len(list2)`

```py
class Solution:
	def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
		if not wordList or endWord != wordList[-1]:
			return 0

		num_match_word = 0
		transformed_wordList = [beginWord]

		for i in range(len(wordList)):
			word_1 = list(transformed_wordList[-1])
			word_2 = list(wordList[i])
			if len(word_1) != len(word_2):
				continue

			for j in range(len(word_1)):
				if word_1[j] == word_2[j]:
					num_match_word += 1

			if num_match_word == len(word_1) - 1:
				transformed_wordList.append(wordList[i])

			num_match_word = 0
			word_1 = []
			word_2 = []

		last_word = list(transformed_wordList[-1])
		num_matched_word = 0
		transformed_word = 0

		for m in range(len(transformed_wordList) - 2, 0, -1):
			previous_word = list(transformed_wordList[m])

			for n in range(len(last_word)):
				if last_word[n] == previous_word[n]:
					num_matched_word += 1

			if num_matched_word == len(last_word) - 1:
				transformed_word += 1
				if transformed_word >= 2:
					transformed_wordList.pop(m + 1)
			num_matched_word = 0
			previous_word = []

		return len(transformed_wordList)
```

## step 2
- 他の方の解答を見る

- 参考①：https://github.com/ksaito0629/leetcode_arai60/pull/19/changes
    - なるほど、1単語をノード、単語の文字の差を距離と捉えて、距離 `1` のノード同士を繋ぐ graph をつくって、開始点から終了点までの最短移動距離を求めるイメージか
	    - プログラムを読むと、単語の中の語を順に * に置換したパターンを作成し、一致するパターンがあるかどうかを見ている

```py
from collections import defaultdict, deque
from typing import List


class Solution:
	def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
		if not wordList or endWord not in wordList:
			return 0

		pattern_to_words = defaultdict(list)

		for word in wordList:
			if len(beginWord) != len(word):
				continue
			for i in range(len(beginWord)):
				pattern = f"{word[:i]}*{word[i + 1:]}"
				pattern_to_words[pattern].append(word)

		def find_shortest_path(start_node: str) -> int:
			distance = 1
			frontier = deque([(start, distance)])
			visited = {start}

			while frontier:
				word, distance = frontier.popleft()
				for i in range(len(beginWord)):
					pattern = f"{word[:i]}*{word[i + 1:]}"
					for next_word in pattern_to_words[pattern]:
						if next_word in visited:
							continue
						if next_word == endWord:
							return distance + 1
						frontier.append((next_word, distance + 1))
						visited.add(next_word)
			return 0

		return find_shortest_path(beginWord)
```
- パターンを作らずに、単語間の非一致の語の数を距離とする graph を作成するアプローチはどうか？
    - この場合の時間計算量は、単語数を `n`, 単語長を `l` とすると
	    - 全ペア比較が`O(n^2)`
		- 各比較で最大 `O(l)`
		- したがって、 graph 構築が最大 `O(n^2 + l)` となる。

- 時間計算量は重いが、書いてみる

```py
class Solution:
	def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
		if not wordList or endWord not in wordList:
			return 0

		words = [beginWord] + wordList
		graph = [[] for _ in range(len(words))]

		def differs_by_one(word1: str, word2: str) -> bool:
			diff = 0
			for character_1, character_2 in zip(word1, word2):
				if character_1 != character_2:
					diff += 1
					if diff > 1:
						return False
			return diff == 1

		for i in range(len(words)):
			for j in range(i + 1, len(words)):
				if differs_by_one(words[i], words[j]):
					graph[i].append(j)
					graph[j].append(i)

		start_index = 0
		end_index = words.index(endWord)

		queue = deque([(start_index, 1)])
		visited = [False] * len(words)
		visited[start_index] = True

		while queue:
			node, steps = queue.popleft()

			if node == end_index:
				return steps

			for neighbor in graph[node]:
				if not visited[neighbor]:
					visited[neighbor] = True
					queue.append((neighbor, steps + 1))

		return 0
```
- やはり重いため、実務の観点では現実的な解ではないか
- また別の観点でのアプローチとして、単語の各位置を `a-z` に置き換える解法もある

```py
class Solution:
	def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
		words = set(wordList)

		if endWord not in words:
			return 0

		queue = deque([(beginWord, 1)])

		while queue:
			word, steps = queue.popleft()

			if word == endWord:
				return steps

			for i in range(len(word)):
				for ch in "abcdefghijklmnopqrstuvwxyz":
					if ch == word[i]:
						continue

					next_word = word[:i] + ch + word[i + 1:]

					if next_word in words:
						words.remove(next_word)
						queue.append((next_word, steps + 1))

		return 0
```
- 時間計算量は `O(n * l^2)`
- 空間計算量は `O(n)`
- 問題を解くことにおいては、この解法でも問題ないかもしれない。実務観点では、おそらく使わない

- その他見た PR
	- https://github.com/Shunii85/arai60/pull/20/changes#diff-61f6a80c8e6841cb6919219ebaab2bd5ef628d145469af3602f4613e1d2ad097
	- https://github.com/ksaito0629/leetcode_arai60/pull/19/changes
	- https://github.com/dorxyxki/arai60/pull/20/changes
	- https://github.com/naoto-iwase/leetcode/pull/19/changes#r2427673789


## step 3
- 結局、単語ごとにパターンを作ってパターンに一致する単語一覧をつくる解法が、プログラムの簡易さ、時間計算量の観点で良いと考えた
- ただし、変数名は個人の好みの範囲で、変数名から変数の役割が想起できる変数名に変更

```py
from collections import defaultdict, deque
from typing import List


class Solution:
	def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
		if endWord not in wordList:
			return 0

		words_by_pattern = defaultdict(list)
		for word in wordList:
			for i in range(len(word)):
				pattern = f"{word[:i]}*{word[i + 1:]}"
				words_by_pattern[pattern].append(word)

		queue = deque([(beginWord, 1)])
		visited_words = {beginWord}

		while queue:
			current_word, steps = queue.popleft()

			for i in range(len(current_word)):
				pattern = f"{current_word[:i]}*{current_word[i + 1:]}"

				for next_word in words_by_pattern[pattern]:
					if next_word == endWord:
						return steps + 1

					if next_word not in visited_words:
						visited_words.add(next_word)
						queue.append((next_word, steps + 1))

				words_by_pattern[pattern] = []

		return 0
```
