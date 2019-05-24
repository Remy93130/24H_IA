import os
import sys

from network import Network
from game import Game

TEAM_NAME = "ascii_p<array>"

ILLEGAL_US = "joué illégal"
ILLEGAL_OTHER = "adversaire illegal"
ENDED = "Terminée"

class Main(object):
	def __init__(self, ip, port):
		if type(port) == str:
			try:
				self.port = int(port)
			except:
				raise Exception("La valeur du port est incorrecte.")
		else:
			self.port = port

		self.ip = ip

		self.net = Network(self.ip, self.port)
		self.game = Game(self.net.sendFirstMessage(TEAM_NAME))

	def run(self):
		first = True

		while True:
			rcvd = self.net.receive()
			print("$" + rcvd)
			choose = None

			if ILLEGAL_US in rcvd:
				choose = self.game.turn(illegalUs=True)
			elif ILLEGAL_OTHER in rcvd:
				choose = self.game.turn(illegalOther=True)
			elif ENDED in rcvd:
				break
			else:
				choose = self.game.turn(rcvd=rcvd, first=first)
				first = False

			print(choose)
			self.net.send(choose)


if __name__ == "__main__":
	m = Main(sys.argv[1], sys.argv[2])
	print("Début de partie.\n")
	m.run()
	print("Partie terminée.\n")

