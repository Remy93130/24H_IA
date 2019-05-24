import socket


class Network:
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.sock = self._connectTo()

	def _connectTo(self):
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((self.ip, self.port))
			return sock
		except Exception as e:
			raise Exception("Connexion impossible à {} au port {}\n\n{}".format(self.ip, self.port, e))

	def sendFirstMessage(self, message):
		self.send(message)
		return self.receive()

	def receive(self):
		try:
			data = self.sock.recv(2048)   # On tente une reconnection en cas de déconnexion
		except:
			self.sock = self._connectTo()
			data = self.sock.recv(2048)

		return data.decode()

	def send(self, data):
		data = data.encode()

		try:
			self.sock.send(data)   # On tente une reconnection en cas de déconnexion
		except:
			self.sock = self._connectTo()
			self.sock.send(data)
