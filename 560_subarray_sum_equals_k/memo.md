## step 1
### アプローチ

- Constraints
- 1 <= nums.length <= 2 * 10^4
- -1000 <= nums[i] <= 1000
- -10^7 <= k <= 10^7

```
（以下構想）-> 発想が Two Sum 寄りであり、区間の合計を求める設計になっていないため、以下のアプローチでは解けない
- 与えられる配列の最大長が 2 * 10^4 であるため、考えうるすべての組み合わせ n(n + 1) / 2 を試すのは時間計算量の観点から現実的ではない（python では１秒間の計算量が高々10^7程度であるため、TLE となる）。
- 代案としては、前から順に要素を一つずつ見ていく → int との差をとる -> 差 = 要素となる要素があれば、~~カウンタを 1 増やす、といった解法が考えられる~~ 配列に要素の組を追加する
-> ただし、連続する部分配列である必要があるため、要素の順序を保持しておく必要がある -> `dict` or `OrderedDict` を使う？
-> 差が0になるまで繰り返し処理を行うような設計とする？
- 戻り値は、配列の長さを返す -> 解となる要素の値またはペアを要素として持つ配列を作成する -> defaultdict(list) を使う

↓
調べたところ、累積和をキー、累積和の出現回数を値として持つ辞書を作成する解法がある

```

from collections import defaultdict
from typing import List


class Solution:
	def subarraySum(self, nums: List[int], k: int) -> int:
		count = 0
		current_sum = 0
		prefix_count = defaultdict(int)  # item の個数または頻度を値として持つ場合に使う
		prefix_count[0] = 1  # 何も選ばない時点で、累積和　0 が１回ある、とみなす

		for num in nums:
			current_sum += num
			count += prefix_count[current_sum - k]
			prefix_count[current_sum] += 1

		return count

## step 2
- 他の人の解法も見てみる
	- https://github.com/tom4649/Coding/pull/15
	- https://github.com/dorxyxki/arai60/pull/16/changes
- など見てみたが、最終的な解法は同じであった

- 累積和の考え方を用いた具体例をメモ
	- https://discord.com/channels/1084280443945353267/1183683738635346001/1192145962479665304
        > いや、累積和を日常で見る機会ってあると思うんですよ。たとえばですけれども、電車の各駅の距離とかかる時間が書かれていて、ちょうど10分かかる駅の組み合わせはどれか、といわれたら、(これはマイナスが出ないので更に楽ですが、)終着駅から出発する電車が、どこを何時何分に通過するかを書き出しながら、その10分前に別の駅にいたかを確認したらいいですよね。

- 写経

class Solution:
	def subarraySum(self, nums: list[int], k: int) -> int:
		count = 0
		current_sum = 0
		prefix_count = defaultdict(int)
		prefix_count[0] = 1

		for num in nums:
			current_sum += num
			count += prefix_count[current_sum - k]
			prefix_count[current_sum] += 1

		return count

## 感想
- 自力で累積和を用いて解く解法は思い浮かばなかったが、考え方を理解すると、１分もかからずに書くことができる
- 累積和自体の概念は知っていたが、「累積和を使って解けるのでは」というところまでには至らなかった。まだ理解ができていないということか。
