
us = True


class Player(object):
	def __init__(self):
		global us

		self.id = 0 if not us else 1
		us = False
		self.previous = None
		self.score = 0

	def addToScore(self, toAdd):
		self.score += toAdd

	def __hash__(self):
		return self.id

	def __eq__(self, other):
		return other and self.id == other.id





