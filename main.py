import os
import sys
import socket

from network import Network
from game import Game
from logs import logger

TEAM_NAME = "ascii_p<array>"

ILLEGAL_US = "21"
ILLEGAL_US2 = "91"
TO_US_TO_PLAY = "10"
NORMAL_OTHER = "20"
ILLEGAL_OTHER = "22"
START = "01"
ENDED = "Fin de la partie"


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
		toPars = self.net.sendFirstMessage(TEAM_NAME)
		with open("chaine.txt", "w") as w:
			w.write(toPars)

		self.game = Game(toPars)

	def run(self):
		first = True

		while True:
			logger.info("Socket en écoute")
			rcvd = self.net.receive()
			logger.info("Socket a recu {}".format(rcvd))
			print("$" + rcvd, end=" - ")
			choose = None

			if ILLEGAL_US in rcvd or ILLEGAL_US2 in rcvd:
				self.game.turn(illegalUs=True)
				continue
			elif ILLEGAL_OTHER in rcvd:
				self.game.turn(illegalOther=True)
				continue
			elif NORMAL_OTHER in rcvd:
				self.game.turn(rcvd=rcvd, other=True)
				continue
			elif ENDED in rcvd:
				break
			elif START in rcvd:
				self.game.turn(rcvd=rcvd, first=first)
				first = False
				continue
			elif TO_US_TO_PLAY in rcvd:
				choose = self.game.turn(rcvd=rcvd)
			else:
				continue

			print(choose)
			self.net.send(choose)


if __name__ == "__main__":
	m = Main(sys.argv[1], sys.argv[2])
	print("Début de partie.\n")
	m.run()
	print("Partie terminée.\n")

