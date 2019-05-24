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
		
	def isBlocked(self):
		return self.parcelle.blocked or self.coffee
		
	def i(self):
		return position.row
		
	def j(self):
		return position.column
		
	def sameParcel(self,cell):
		return self.parcelle == cell.parcelle 

	""" Ajouter spécificités des cases ici"""

class Parcel(object):
	def __init__(self,blocked):
		self.cells = set()
		self.blocked = blocked

	def add(self,cell):
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
	def __init__(self, height, width, parcels):
		print(type(height), type(width))
		self.height = height
		self.width = width
		self.board = {}

		self._initBoard()

	def _initBoard(self,parcels):
		for row in range(self.height):
			for column in range(self.width):
				self.board[Position(row, column)] = Cell(Position(row, column))
				
	def updateBoard(self, parcels):
		for parcel in parcels :
			p = Parcel('blocked' in parcel)
			parcel.discard('blocked')
			for cell in parcel :
				p.add(self.board[Position(cell[0],cell[1])])
				self.board[Position(cell[0],cell[1])].setParcelle(p)
				
	def updateCell(self,position,player):
		self.board[position].setCoffee(player)

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
				
	def availableCells(self,previouses):
		available = set()
		if not previouses[0]: #premier tour
			for i in self.board.values():
				if not i.isBlocked :
					available.add(i)
			return available
		current = previouses[0]
		previous = previouses[1]
		if not previouses[1] :
			previous = current
		for i in range(self.width):
			cell = self.board[Position(i,current.j())]
			if not cell.isBlocked() and \
			not cell.sameParcel(current) and \
			not cell.sameParcel(previous) :
				available.add(cell)
		for j in range(self.width):
			cell = self.board[Position(current.i(),j)]
			if not cell.isBlocked() and \
			not cell.sameParcel(current) and \
			not cell.sameParcel(previous) :
				available.add(cell)
		return available
		
			
				








