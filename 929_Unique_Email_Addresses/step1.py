# !/usr/bin/env python3

class Solution:
	def numUniqueEmails(self, emails: list[int]) -> list[int]:
		local_name = {}
		domain_name = {}

		for i, str in enumerate(emails):
			local, domain = str.split("@", 1)
			local = local.split("+", 1)[0].replace(".", "")
			local_name[i] = local
			domain_name[i] = domain

		unique = set()
		for i in range(len(emails)):
			unique.add(f"{local_name[i]}@{domain_name[i]}")

		return len(unique)
