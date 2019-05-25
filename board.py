from player import Player
from logs import logger

# logger.info

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
		return self.position.__str__()

	def __repr__(self):
		return self.position.__str__()

	def isBlocked(self):
		return self.parcelle.blocked or self.coffee

	def i(self):
		return self.position.row

	def j(self):
		return self.position.column
		
	def sameParcel(self,cell):
		return self.parcelle == cell.parcelle
		
	def coffeeInParcel(self,player):
		count = 0
		for cell in self.parcelle.cells:
			if cell.coffee == player:
				count += 1
		return count

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
				
	def updateBoard(self, msg):
		parcels = parseMsg(msg)
		for parcel in parcels :
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
	
	def strWithCells(self,available):
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
		
class IA(object):
	def __init__(self,board,previous,player):
		self.available = board.availableCells(previous)
		self.board = board
		self.player = player
		
	def choice(self):
		logger.info(self.board.strWithCells(self.available))
		self.getWinningCells()
		logger.info(self.board.strWithCells(self.available))
		self.getWhereMore()
		logger.info(self.board.strWithCells(self.available))
		self.getBiggest()
		logger.info(self.board.strWithCells(self.available))
		self.getCellsWithNeighbours()
		logger.info(self.board.strWithCells(self.available))
		return self.alea()
	
	def alea(self):
		if len(self.available) == 0: return None
		return self.available.pop()		
	
	def getWhereMore(self):
		more = {}
		maxi = 0
		more[0] = set()
		for cell in self.available:
			size = cell.coffeeInParcel(self.player)
			if size > maxi : maxi = size
			if size not in more: more[size] = set()
			more[size].add(cell)
		self.available = more[maxi]
		
	def getBiggest(self):
		biggest = {}
		maxi = 0
		biggest[0] = set()
		for cell in self.available:
			size = len(cell.parcelle.cells)
			if size > maxi : maxi = size
			if size not in biggest: biggest[size] = set()
			biggest[size].add(cell)
		self.available = biggest[maxi]
		
	def getCellsWithNeighbours(self):
		withNeighbours = set()
		for cell in self.available:
			for direction in ((1, 0), (0, 1), (-1, 0), (0, -1)) :
				neighbour = Position(cell.i()+direction[0], cell.j()+direction[1])
				if neighbour.row > 9 or neighbour.row < 0 or neighbour.column > 9 or neighbour.column < 0 : continue 
				if self.board[neighbour].coffee == self.player :
					withNeighbours.add(cell)
					break
		if withNeighbours : self.available = withNeighbours
		
	def getWinningCells(self):
		winningCells = set()
		for cell in self.available:
			size = len(cell.parcelle.cells)
			coffee = cell.coffeeInParcel(self.player)
			if (size / 2) < coffee + 1:
				winningCells.add(cell)
		if winningCells : self.available = winningCells
					
	
		
def parseMsg(msg):
	
	def second(matrix, notYet, cell, parcel) :
		for direction in ((1, 0), (0, 1), (-1, 0), (0, -1)) :
			moveOn = (cell[0]+direction[0], cell[1]+direction[1])
			if moveOn in notYet :
				if canMove(cell, matrix, direction) :
					parcel.add(moveOn)
					notYet.remove(moveOn)
					second(matrix, notYet, moveOn, parcel)

	def canMove(cell, matrix, direction) :
		cell_x = cell[0]
		cell_y = cell[1]
		dir_x = direction[0]
		dir_y = direction[1]
		if dir_x == 1 : return cell_x < 9 and matrix[cell_x][cell_y][4] == '0'#bas
		if dir_x == -1 : return cell_x > 0 and matrix[cell_x][cell_y][6] == '0' #haut
		if dir_y == 1 : return cell_y < 9 and matrix[cell_x][cell_y][3] == '0' #droite
		if dir_y == -1 : return cell_y > 0 and matrix[cell_x][cell_y][5] == '0' #gauche

	def isUnplayable(matrix, cell) : 
		return int(matrix[cell[0]][cell[1]][:2]) != 0
	
	lines = msg.split('|')
	matrix = []
	for line in lines:
		matrix.append(line.split(':'))
	for i in range(10):
		for j in range(10):
			matrix[i][j] = '{0:07b}'.format(int(matrix[i][j]))
			
	parcels = []

	notYet = set()
	for i in range(10):
		for j in range(10):
			notYet.add((i, j))

	while notYet :
		cell = notYet.pop()

		parcel = set()

		if (isUnplayable(matrix, cell)) :
			parcel.add('blocked')
			
		parcel.add(cell)
		
		second(matrix, notYet, cell, parcel)
		parcels.append(parcel)

	return parcels


board = Board(10, 10)
board.updateBoard('3:9:71:69:65:65:65:65:65:73|2:8:3:9:70:68:64:64:64:72|6:12:2:8:3:9:70:68:64:72|11:11:6:12:6:12:3:9:70:76|10:10:11:11:67:73:6:12:3:9|14:14:10:10:70:76:7:13:6:12|3:9:14:14:11:7:13:3:9:75|2:8:7:13:14:3:9:6:12:78|6:12:3:1:9:6:12:35:33:41|71:77:6:4:12:39:37:36:36:44|')

players = [Player(), Player()]
turn = 0

previous = [None, None, None]

for i in range(35):
	print(turn)
	ia = IA(board,previous,players[turn])
	choice = ia.choice()
	print(choice)
	board.updateCell(choice.position, players[turn])
	previous.append(choice)
	turn = (turn + 1)%2
