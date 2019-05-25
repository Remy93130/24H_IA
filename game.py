from random import choice

from board import Position, Cell, Path, Board
from player import Player

LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
NUMBERS = list(range(1, 11))

class Game(object):
	def __init__(self, teamName, height=10, width=10):
		self.board = Board(height, width)
		self.teamName = teamName
		self.player1 = Player()
		self.player2 = Player()
		self.score = 0

		self.previous = [None, None]

	def getScore(self):
		return self.score

	def addScore(self, added):
		self.score += added

	def addPrevious(self, cell):
		self.previous.append(cell)

	def removeLastPrevious(self):
		return self.previous.pop(-1)

	def parseRcvdPosition(self, rcvd):
		splited = rcvd.split(":")

		return Position.create(splited[-2], splited[-1])


	def turn(self, rcvd=None, first=False, illegalUs=False, illegalOther=False, other=False):
		if illegalUs: # Si on a mal joué au tour d'avant
			cell = self.removeLastPrevious()
			self.board.updateCell(cell.position, None)
			return  # Enlever le coup qu'on a fait avant

		if illegalOther:
			return

		if other and rcvd is not None:  # Update la position de l'adversaire
			self.board.updateCell(self.parseRcvdPosition(rcvd), self.player2)
			return

		if first and rcvd is not None:
			self.board.updateBoard()

		if rcvd is not None:
			self.board






		# return self.alea()

	def alea(self):
		return choice(LETTERS) + ":" + str(choice(NUMBERS))
