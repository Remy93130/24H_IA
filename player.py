
counter = 0


class Player(object):
	def __init__(self, position):
		self.position = position

		global counter
		counter += 1
		self.id = counter

	def __hash__(self):
		return self.id

	def __eq__(self, other):
		return self.id == other.id



