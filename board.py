import test

LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]


class Position(object):
	def __init__(self, row, column):
		self.row = row
		self.column = column
		self.pos = (row, column)

	def get(self):
		return self.pos

	def export(self):
		return LETTERS[self.column]  + ":" + str(self.row + 1)

	@staticmethod
	def create(s1, s2):
		y = None

		for i, letter in enumerate(LETTERS):
			if letter == s1:
				y = i

		x = int(s2) - 1

		return Position(x, y)



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

	def __repr__(self):
		return self.position.__str__()

	def isBlocked(self):
		return self.parcelle.blocked or self.coffee

	def i(self):
		return self.position.row

	def j(self):
		return self.position.column

	def sameParcel(self, cell):
		return self.parcelle == cell.parcelle

	""" Ajouter spécificités des cases ici"""


class Parcel(object):
	def __init__(self, blocked):
		self.cells = set()
		self.blocked = blocked

	def add(self, cell):
		self.cells.add(cell)

	def __contains__(self, item):
		return item in self.cells


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
		self.parcels = set()

		self._initBoard()

	def _initBoard(self):
		for row in range(self.height):
			for column in range(self.width):
				self.board[Position(row, column)] = Cell(Position(row, column))

	def updateBoard(self, parcels):
		for parcel in parcels:
			p = Parcel('blocked' in parcel)
			parcel.discard('blocked')
			self.parcels.add(p)
			for cell in parcel:
				p.add(self.board[Position(cell[0], cell[1])])
				self.board[Position(cell[0], cell[1])].setParcelle(p)

	def updateCell(self, position, player):
		self.board[position].setCoffee(player)

	def __getitem__(self, item):
		return self.board[item]

	def __setitem__(self, key, value):
		self.board[key] = value

	def __str__(self):
		s = ""

		array = []
		for i in range(10):
			array2 = []
			for j in range(10):
				array2.append(0)
			array.append(array2)

		count = 0
		for parcel in self.parcels:
			if parcel.blocked:
				char = chr(count + ord('A'))
			else:
				char = chr(count + ord('a'))
			for cell in parcel.cells:
				array[cell.i()][cell.j()] = char
			count += 1

		for line in array:
			for e in line:
				s += e
			s += '\n'

		return s

	def strWithAvailable(self, available):
		s = ""

		array = []
		for i in range(10):
			array2 = []
			for j in range(10):
				array2.append(0)
			array.append(array2)

		count = 0
		for parcel in self.parcels:
			if parcel.blocked:
				char = chr(count + ord('A'))
			else:
				char = chr(count + ord('a'))
			for cell in parcel.cells:
				if cell in available:
					array[cell.i()][cell.j()] = '*'
				else:
					array[cell.i()][cell.j()] = char
			count += 1

		for line in array:
			for e in line:
				s += e
			s += '\n'

		return s

	def __repr__(self):
		return self.__str__()

	def browseAll(self):
		for r in range(self.height):
			for c in range(self.width):
				p = Position(r, c)
				yield p, self[p]

	def availableCells(self, previouses):
		available = set()
		if not previouses[-1]:  # premier tour
			for i in self.board.values():
				if not i.isBlocked():
					available.add(i)
			return available
		current = previouses[-1]
		previous = previouses[-2]
		if not previouses[-2]:
			previous = current
		for i in range(self.width):
			cell = self.board[Position(i, current.j())]
			if not cell.isBlocked() and \
				not cell.sameParcel(current) and \
				not cell.sameParcel(previous):
				available.add(cell)
		for j in range(self.width):
			cell = self.board[Position(current.i(), j)]
			if not cell.isBlocked() and \
				not cell.sameParcel(current) and \
				not cell.sameParcel(previous):
				available.add(cell)
		return available


board = Board(10, 10)
board.updateBoard(test.main(test.genererTab(
	'3:9:71:69:65:65:65:65:65:73|2:8:3:9:70:68:64:64:64:72|6:12:2:8:3:9:70:68:64:72|11:11:6:12:6:12:3:9:70:76|10:10:11:11:67:73:6:12:3:9|14:14:10:10:70:76:7:13:6:12|3:9:14:14:11:7:13:3:9:75|2:8:7:13:14:3:9:6:12:78|6:12:3:1:9:6:12:35:33:41|71:77:6:4:12:39:37:36:36:44|')))
# print(board)
av = board.availableCells([None, None])
print(av)
print(board.strWithAvailable(av))
