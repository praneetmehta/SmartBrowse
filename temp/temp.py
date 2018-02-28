class First(object):
	def __init__(self):
		print("first")

class Second(First):
	def __init__(self):
		super().__init__()
		print ("second")

class Third(First):
	def __init__(self):
		print ("third")

class Fourth(Second, Third):
	def __init__(self):
		super(Fourth, self).__init__()
		print ("that's it")

if 	__name__ == "__main__":
	Fourth()
