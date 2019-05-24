LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]


class Position(object):
	def __init__(self, row, column):
		self.row = row
		self.column = column
		self.pos = (row, column)

	def get(self):
		return self.pos

	def export(self):
		return str(self.row + 1) + ":" + LETTERS[self.column]

	@staticmethod
	def create(s):
		x, y = s.split(":")

	def __str__(self):
		return "({}, {})".format(self.row, self.column)

	def __repr__(self):
		return self.__str__()

	def __hash__(self):
		return hash(self.pos)

	def __eq__(self, other):
		return self.row == other.row and self.column == other.column


class Cell(object):
	def __init__(self, position, parcelle=None):
		self.position = position
		self.parcelle = parcelle
		self.coffee = None

	def setParcelle(self, value):
		self.parcelle = value

	def setCoffee(self, player):
		self.coffee = player

	def __str__(self):
		return "X"

	""" Ajouter spécificités des cases ici"""


class Path(object):
	def __init__(self, pathList):
		self.path = pathList

		if len(self.path) > 0:
			self.base = self.path[0]
			self.to = self.path[-1]
		else:
			self.base = None
			self.to = None

	def __contains__(self, item):
		return item in self.path

	def collide(self, path):
		for position in self.path:
			if position in path:
				return True
		return False

	def collideSameTurn(self, path):
		for i in range(len(self.path)):
			for j in range(len(path.path)):
				if i == j and self.path[i] == path.path[j]:
					return True
		return False


class Board(object):
	def __init__(self, height, width):
		print(type(height), type(width))
		self.height = height
		self.width = width
		self.board = {}

		self._initBoard()

	def _initBoard(self):
		for row in range(self.height):
			for column in range(self.width):
				self.board[Position(row, column)] = Cell(Position(row, column))

	def updateBoard(self, data):
		pass

	def __getitem__(self, item):
		return self.board[item]

	def __setitem__(self, key, value):
		self.board[key] = value

	def __str__(self):
		s = ""

		for r in range(self.height):
			s += " ".join([str(self[Position(r, c)]) for c in range(self.width)])

		return s

	def __repr__(self):
		return self.__str__()

	def browseAll(self):
		for r in range(self.height):
			for c in range(self.width):
				p = Position(r, c)
				yield p, self[p]








