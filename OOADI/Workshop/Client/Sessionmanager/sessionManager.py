import socket
import pickle
import hashlib
import Interface_Soket as iSock
import cryptography
import random
import string
import threading
from cryptography import fernet as f
from clientDB import Client_DB
import os

#############################################################################
#
#                           Class
#
#############################################################################

class UI_Session_Manager(threading.Thread):
	def __init__(self, socket):
		self.loggedin = False
		self.interface = iSock.interface(socket)
		self.Channels = []
		self.path = 'clientData.txt'
		if not os.path.exists(self.path):
			self.clientDB = Client_DB()
			with open('clientData.txt', 'wb') as bente:
				pickle.dump(self.clientDB, bente)
			return
		with open('clientData.txt', 'rb') as bente:
			self.clientDB = pickle.load(bente)

	def createUser(self, username, password):
		self.username = username
		self.password = password
		try:
			salt = "dinMor"
			userpassword = self.password+salt
			hashed = hashlib.md5(userpassword.encode()).hexdigest()
			sendlist = ["createUser",self.username,hashed]
			logindata = pickle.dumps(sendlist)
			check = self.interface.send(logindata)
			print("Create user: ", check)
			return check[1]
		except:
			return False

	def login(self, username, password):
		self.username = username
		self.password = password
		try:
			salt = "dinMor"
			userpassword = self.password+salt
			hashed = hashlib.md5(userpassword.encode()).hexdigest()
			sendlist = ["login",self.username,hashed]
			logindata = pickle.dumps(sendlist,pickle.HIGHEST_PROTOCOL)
			check = self.interface.send(logindata)
			print("Login: ",check)
			if check[1]:
				for channelname in check[2]:
					Channel = UI_Channel_Manager(self.clientDB, channelname)
					Channel.Lookup()
					self.Channels.append([channelname,Channel])
			return check[1], check[2]
		except:
			return False

	def createChannel(self, NameOfChannel):
		sendList = ["createChannel", NameOfChannel]
		sendList = pickle.dumps(sendList)
		check = self.interface.send(sendList)
		print("Create channel: ",check)
		if check[1]:
			Key = f.Fernet.generate_key()
			Key = f.Fernet(Key)
			Channel = UI_Channel_Manager(self.clientDB, str(NameOfChannel), Key)
			Channel.Howtosavealife()
			self.Channels.append([NameOfChannel,Channel])
		return check[1]

	def joinChannel(self, NameOfChannel):
		try:
			sendList = ["joinChannel", NameOfChannel]
			sendList = pickle.dumps(sendList,pickle.HIGHEST_PROTOCOL)
			check = self.interface.send(sendList)
			if check[1]:
				Key = self.createP2PManager()
				Channel = UI_Channel_Manager(self.clientDB, str(NameOfChannel), Key)
				Channel.Howtosavealife()
				self.Channels.append([NameOfChannel,Channel])
		except:
			return False

	def createP2PManager(self):
		Key = 'JabbatheHut'
		return Key

	def forwardMessage(self, message, channel):
		try:
			sendlist = ["logEntry", channel, message]
			sendlist = pickle.dumps(sendlist)
			check = self.interface.send(sendlist)
			return True
		except:
			return False
	
	def logout(self):
		del self

	def encryptMessage(self, key, message):
		encMessage = key.encrypt(message)
		return encMessage
		
	def decrypt(self, key, encmessage):
		message = key.decrypt(encmessage)
		return message

	def get_random_string(self, length):
		# choose from all lowercase letter
		letters = string.printable
		result_str = ''.join(random.choice(letters) for i in range(length))
		return result_str

	def __delete__(self):
		print("Deleted session")

	def receiveMessage(self):
		res = self.interface.listen()
		match res[0]:
			case 'login':
				if (res[1] == False):
					self.password = ""
					self.username = ""
					self.loggedin = False
					return False
				else:
					return True

			case 'createUser':
				if (res[1] == False):
					self.username = ""
					self.password = ""
					return False
				else:
					self.loggedin = True
					return True

			case 'joinChannel':
				if (res[1] == False):
					return False
				else:
					return True

			case 'createChannel':
				return True

			case 'lastChat':
				lastMessage = res[1]
				return lastMessage

			case 'chatLog':
				return res[2]

			case other:
				return False
			

		

#############################################################################
#
#                           Class
#
#############################################################################

class UI_Channel_Manager(UI_Session_Manager):
	def __init__(self,clientDB, channelName, Key=''):
		self.channelLog = []
		self.channelName = channelName
		self.channelKey = Key
		self.Client_DB_manager = clientDB
		

	def sendMessage(message):
		try:
			message = super().encryptMessage(self.key, message)
			super().forwardMessage(message, self.channelName)
			return True
		except:
			return False
			
	def updateLog():
		try:
			pickledLog = Interface_Soket.interface(host, port).send(pickle.dumps(['chatLog', self.channelName]))
			self.channelLog = pickle.loads(pickledLog)
			return self.channelLog
		except:
			return False

	def Howtosavealife(self):
		self.Client_DB_manager.createChannel(self.channelName, self.channelKey)
		with open('clientData.txt', 'wb') as bente:
			pickle.dump(self.Client_DB_manager, bente)
	
	def Lookup(self):
		self.channelKey = self.Client_DB_manager.lookup(key='Channel_key',channel=self.channelName)




#############################################################################
#
#                           Initial test things
#
#############################################################################

class connectionSocket:
	def __init__(self, port):
		self.port = port
		self.host = "127.0.0.1"


	def echo(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect((self.host, self.port))
			s.sendall(b"Hello, world")
			data = s.recv(1024)
		print(f"Received {data!r}")

#############################################################################
#
#                           Execution if main
#
#############################################################################

# if __name__ == "__main__":
#     client = UI_Session_Manager()
#     client.login("mads", "dinmor")
#     client.receiveMessage()





