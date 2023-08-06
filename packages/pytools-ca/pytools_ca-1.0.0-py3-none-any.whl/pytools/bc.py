class wait:
	class broadcast:
		def __init__(self, broadcast, root):
			while True:
				if root[broadcast]:
					break
				else:
					continue
			return
		def always(func, broadcast, root):
			while True:
				if root[broadcast]:
					break
				else:
					continue
			func()
	def __init__(self):
		self.bc = broadcast()
	class var:
		def __init__(self, var, value):
			while True:
				if globals()[var] == value:
					break
				else:
					continue
			return
		def always(func, var, value):
			while True:
				if globals()[var] == value:
					break
				else:
					continue
			func()