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
import signal
from p2pClass import p2pClass as p2p

#############################################################################
#
#                           Class
#
#############################################################################

class UI_Session_Manager(threading.Thread):
	def __init__(self, socket):
		self.loggedin = False
		self.interface = iSock.interface(socket)
		self.queue = []
		self.event = threading.Event()
		thread2 = threading.Thread(target=self.receiveMessage, )
		thread2.start()
		self.p2p = p2p()
		
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
			self.interface.send(logindata)

			event_createUser = self.event.wait(10)
			if event_createUser:
				print(self.queue)
				for message in self.queue:
					if message[0] == 'createUser':
						index = self.queue.index(message)
						ret = self.queue.pop(index)
						self.event.clear()
						print(ret)
						return ret[1]
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
			print(1)
			event_createUser = self.event.wait(10)
			print(2)
			if event_createUser:
				print(3)
				for message in self.queue:
					print(message)
					if message[0] == 'login':
						self.event.clear()
						if message[1]:
							index = self.queue.index(message)
							ret = self.queue.pop(index)
							for channelname in ret[2]:
								Channel = UI_Channel_Manager(self.clientDB, channelname)
								Channel.Lookup()
								print("Login: ", ret)
								self.Channels.append([channelname,Channel])
							return ret[1], ret[2]
				return False
			else:
				return False
		except:
			return False

	def createChannel(self, NameOfChannel):
		sendList = ["createChannel", NameOfChannel]
		sendList = pickle.dumps(sendList)
		self.interface.send(sendList)

		event_createUser = self.event.wait(10)
		if event_createUser:
			for message in self.queue:
				if message[0] == 'createChannel' and message[1] == True:
					index = self.queue.index(message)
					ret = self.queue.pop(index)
					self.event.clear()
					Key = f.Fernet.generate_key()
					Key = f.Fernet(Key)
					Channel = UI_Channel_Manager(self.clientDB, str(NameOfChannel),Key)
					Channel.Howtosavealife()
					return ret[1]
			return False
		else:
			return False

	def joinChannel(self, NameOfChannel):
		try:
			sendList = ["joinChannel", NameOfChannel]
			sendList = pickle.dumps(sendList,pickle.HIGHEST_PROTOCOL)
			self.interface.send(sendList)
			event_createUser = self.event.wait(10)
			if event_createUser:
				for message in self.queue:
					if message[0] == 'createUser' and message[1]  == True:
						index = self.queue.index(message)
						self.queue.pop(index)
						self.event.clear()

						Key = self.P2Preceive(NameOfChannel)

						Channel = UI_Channel_Manager(self.clientDB, str(NameOfChannel),Key)
						Channel.Howtosavealife()
						return True
				return False
			else:
				return False
		except:
			return False

	def updateChannel(self, Channel):
		sendList = ["chatLog", Channel]
		sendList = pickle.dumps(sendList)
		self.interface.send(sendList)
		event_update = self.event.wait(10)
		if event_update:
			for message in self.queue:
				if message[0] == 'chatLog':
					index = self.queue.index(message)
					ret = self.queue.pop(index)
					self.event.clear()
					return ret[1]


		

	def P2Psend(self, private, public, channel):

		key = self.clientDB.lookup("Channel_key", channel, False)
		self.p2p.Sending(private, public, key)
		return

	def P2Preceive(self, channel):
		sendlist = ["p2p", channel]
		self.interface.send(pickle.dumps(sendlist))
		return self.P2Preceive()



	def sendMessage(self, message, channel):
		try:
			print(1)
			key = self.clientDB.lookup("Channel_key", channel, False)
			print(key)
			message = self.encryptMessage(key, message)
			print(message)
			sendlist = ["logEntry", channel, message]
			print(sendlist)
			sendlist = pickle.dumps(sendlist)
			check = self.interface.send(sendlist)
			return
		except:
			return False
	
	def logout(self):
		del self

	def encryptMessage(self, key, message):
		print("encrypt")			
		encMessage = key.encrypt(pickle.dumps(message))
		print("encrypted")
		return encMessage
		
	def decrypt(self, ret):
		#! DUMPS måske
		key = self.clientDB.lookup("Channel_key", ret[0], False)
		ret[1][1] = pickle.loads(key.decrypt(ret[1][1]))
		return ret[1][1]

	def get_random_string(self, length):
		# choose from all lowercase letter
		letters = string.printable
		result_str = ''.join(random.choice(letters) for i in range(length))
		return result_str

	def __delete__(self):
		print("Deleted session")

	def receiveMessage(self):
		#!HER SKAL DER LAVES THREDING TING
		#!HER SKAL DER LAVES THREDING TING
		#!HER SKAL DER LAVES THREDING TING
		#!HER SKAL DER LAVES THREDING TING
		#!HER SKAL DER LAVES THREDING TING
		#!HER SKAL DER LAVES THREDING TING
		#!HER SKAL DER LAVES THREDING TING
		#!HER SKAL DER LAVES THREDING TING
		#!HER SKAL DER LAVES THREDING TING
		#!HER SKAL DER LAVES THREDING TING
		#!HER SKAL DER LAVES THREDING TING
		while True:
			res = self.interface.listen()
			print("Receive function: ",res)
			match res[0]:
				case 'login':
					if (res[1] == False):
						self.password = ""
						self.username = ""
						self.loggedin = False
						self.event.set()
					else:
						self.queue.append(res)
						self.event.set()

				case 'createUser':
					if (res[1] == False):
						self.username = ""
						self.password = ""
						self.queue.append(res)
						self.event.set()
					else:
						self.queue.append(res)
						self.event.set()

				case 'joinChannel':
					if (res[1] == False):
						self.queue.append(res)
						self.event.set()
					else:
						self.queue.append(res)
						self.event.set()

				case 'createChannel':
					if res[1] == False:
						self.queue.append(res)
						self.event.set()
					else:
						self.queue.append(res)
						self.event.set()

				case 'chatLog':
					if res[1] == False:
						self.queue.append(res)
						self.event.set()
					else:
						self.queue.append(res)
						self.event.set()

				case 'logEntry':
					self.queue.append(res)

				case 'p2pRequest':
					self.P2Psend(res[1], res[2], res[3])

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
		

	def sendMessage(self, message):
		try:
			message = super().encryptMessage(self.key, message)
			super().forwardMessage(message, self.channelName)
			return True
		except:
			return False
			
	def updateLog(self):

		#!HER SKAL DER LAVES THREDING TING
		#!HER SKAL DER LAVES THREDING TING
		#!HER SKAL DER LAVES THREDING TING

		try:
			iSock.interface(host, port).send(pickle.dumps(['chatLog', self.channelName]))
			event_createUser = self.event.wait(10)
			if event_createUser:
				for message in self.queue:
					if message[0] == 'chatLog':
						self.event.clear()
						return message[1]
				return False
			else:
				return False
		except:
			return False
		#!HER SKAL DER LAVES THREDING TING
		#!HER SKAL DER LAVES THREDING TING
		#!HER SKAL DER LAVES THREDING TING

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

def testclient(session):
	client.createUser("mads", "dinmor")
	# client.createChannel("EnAfOs")




#############################################################################
#
#                           Execution if main
#
#############################################################################



if __name__ == "__main__":
	client = UI_Session_Manager(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

	thread1 = threading.Thread(target=testclient, args=(client, ))

	thread1.start()





