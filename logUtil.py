class Log:
	def __init__(self, level = 2):
		self.logLevelAllowed = level

	def log(self, item, logLevel=0):
		if logLevel >= self.logLevelAllowed:
			print(item)
		else:
			pass
	@property
	def level(self):
		return self.logLevelAllowed

	@level.setter
	def level(self, value):
		self.logLevelAllowed = value