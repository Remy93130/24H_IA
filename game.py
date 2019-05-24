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

	def getPlayers(self):
		return tuple(self.players)

	def getScore(self):
		return self.score

	def addPlayer(self, player):
		self.players.append(player)

	def addScore(self, added):
		self.score += added

	def turn(self, rcvd=None, first=False, illegalUs=False, illegalOther=False):
		return self.alea()

	def alea(self):
		return choice(LETTERS) + ":" + str(choice(NUMBERS))
