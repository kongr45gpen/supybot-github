class Theme(object):
	def __init__(self, repository, brackets = "()"):
		self.msgs = []
		self.repoInfo = repository
		self.repoId = repository['id']
		self.brackets = brackets

	def finalize(self):
		pass

	def enclose(self, text):
		if text == None or text == '':
			#TODO: Remove the space before the URL
			return ""
		return "%s%s%s" % (self.brackets[0], text, self.brackets[1])
