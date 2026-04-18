from collections import defaultdict, deque


class Solution:
	def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
		if endWord not in wordList or not wordList:
			return 0

		words_by_pattern = defaultdict(list)

		for word in wordList:
			for i in range(len(word)):
				pattern = f"{word[:i]}*{word[i + 1:]}"
				words_by_pattern[pattern].append(word)

		word_and_level = deque([(beginWord, 1)])
		visited = set()
		visited.add(beginWord)

		while word_and_level:
			current_word, level = word_and_level.popleft()
			for i in range(len(current_word)):
				pattern = f"{current_word[:i]}*{current_word[i + 1:]}"
				for word in words_by_pattern[pattern]:
					if word == endWord:
						return level + 1
					if word not in visited:
						visited.add(word)
						word_and_level.append((word, level + 1))

		return 0
