from board import Position, Box, Path, Board
from player import Player
from history import History


class Game(object):
	def __init__(self, height, width):
		self.board = Board(height, width)
		self.players = []
		self.score = 0

	def getPlayers(self):
		return tuple(self.players)

	def getScore(self):
		return self.score

	def addPlayer(self, player):
		self.players.append(player)

	def addScore(self, added):
		self.score += added



