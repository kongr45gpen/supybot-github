class Theme(object):
	def __init__(self, repository, brackets = "()"):
		self.msgs = []
		self.repoInfo = repository
		self.brackets = brackets

	def finalize(self):
		pass

	def enclose(self, text):
		return "%s%s%s" % (self.brackets[0], text, self.brackets[1])
