

class History(object):
	def __init__(self, players):
		self.status = {}
		self.playerPositions = {}
		self.playerCommands = {}

		self._loadPlayers(players)

	def _loadPlayers(self, players):
		for p in players:
			self.status[p] = []
			self.playerPositions[p] = []
			self.playerCommands[p] = []

	def getStatus(self, player):
		return self.status[player]

	def getPlayerPositions(self, player):
		return self.playerPositions[player]

	def getPlayerCommands(self, player):
		return self.playerCommands[player]

	def addStatus(self, player, s):
		self.status[player].append(s)

	def addPlayerPosition(self, player, p):
		self.playerPositions[player].append(p)

	def addPlayerCommand(self, player, c):
		self.playerCommands[player].append(c)

