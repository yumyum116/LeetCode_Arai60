# step2.py の修正版
# メールアドレスに @ が２文字以上含まれるケースを想定

class Solution:
	def numUniqueEmails(self, emails: list[str]) -> int:
		if not emails:
			return 0

		unique_emails = set()

		for email in emails:
			local, domain = self.split_email(email)  # 自作関数。タプルをアンパックする

			if self.is_quoted(local):		# あるデータや文字列が引用符で囲まれているかをチェックするための bool型プロパティとして使われる命名規則
				local_content = local[1:-1]
				canonicalized_local = local_content

			else:
				local = local.split('+')[0]  # split の戻り値はリストのため、先頭の要素のみを返す
				canonicalized_local = local.replace('.','')

			canonicalized_email(f"{canonicalized_local}@{domain}")

			unique_emails.add(canonicalized_email)

		return len(unique_emails)

	def split_email(self, email: str) -> tuple[str, str]:
		in_quotes = False
		escape = False
		for i, char in enumerate(email):
			if escape:
				escape = False
				continue
			if char == '\\':
				escape = True
				continue
			if char == '"':
				in_quotes = not in_quotes
				continue
			if char == '@' and not in_quotes:
				return email[:i], email[i+1:]
		# 引用符で囲まれていない '@' が存在しない場合
		return email, ""


	"""

	ローカル部分が引用符で囲まれているかどうかを判定する関数

	"""

	def is_quoted(self, local: str) -> bool:
		return len(local) >= 2 and local.startswith('"') and local.endswith('"')


# step1.py の修正版
# !/usr/bin/env python3

class Solution:
	def numUniqueEmails(self, emails: list[int]) -> list[int]:
		local_name = {}
		domain_name = {}

		for i, str in enumerate(emails):
			local, domain = str.rsplit("@", 1)
			local_without_plus = local.split("+", 1)[0]
			local_without_dot = local_without_plus.replace(".", "")
			local_name[i] = local_without_dot
			domain_name[i] = domain

		unique = set()
		for i in range(len(emails)):
			unique.add(f"{local_name[i]}@{domain_name[i]}")

		return len(unique)


#################################

	正規表現 version

#################################

class Solution:
	def numUniqueEmails(self, emails: list[str]) -> int:
		unique_address_set = set()
		for address in emails:
			local, domain = address.rsplit("@", 1)
			plus_ignored_local = re.sub(r'\+.*', '', local)    # raw 文字列記法を表す 'r'。 'r'を前置した文字列リテラル内では、python 文字列が解釈されない一方で、正規表現の解釈は残るため、'+' を文字として扱うために r'\+' と記述する。
			dot_removed_local = re.sub(r'\.', '', plus_ignored_local)
			unique_address_set.add(f"{dot_removed_local}@{domain}")

		return len(unique_address_set)
