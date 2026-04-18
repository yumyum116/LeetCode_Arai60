# {単語の文字の差 = 距離} と捉えて、距離 1 のノード同士を繋ぐ graph を作成する。

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
			frontier = deque([(start_node, distance)])
			visited = {start_node}

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
