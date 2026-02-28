class Solution:
	def numUniqueEmails(self, emails: list[str]) -> int:
		if not emails:
			return 0

		unique_emails = set()

		for address in emails:
			local_name, domain_name = address.split('@',1)
			normalized_local_name = local_name.split('+', 1)[0].replace(".", "")
			unique_emails.add(f"{normalized_local_name}@{domain_name}")

		return len(unique_emails)
