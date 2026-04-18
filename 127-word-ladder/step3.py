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

		frontier = deque([(beginWord, 1)])
		visited_words = {beginWord}

		while frontier:
			current_word, level = frontier.popleft()

			for i in range(len(current_word)):
				pattern = f"{current_word[:i]}*{current_word[i + 1:]}"

				for next_word in words_by_pattern[pattern]:
					if next_word == endWord:
						return level + 1
					if next_word not in visited_words:
						visited_words.add(next_word)
						frontier.append((next_word, level + 1))

				words_by_pattern[pattern] = []

		return 0
