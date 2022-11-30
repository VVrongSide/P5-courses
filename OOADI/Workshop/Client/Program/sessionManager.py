import socket
import pickle
import hashlib
import Interface as iSock
import cryptography
import random
import string
import threading
from cryptography import fernet as f
from clientDB import Client_DB
import os
import signal
from p2p import p2pClass as p2p

#############################################################################
#
#                           Class
#
#############################################################################

"""
A session manager handling communication of the client sides application with the chat server of the system.
"""
class UI_Session_Manager(threading.Thread):
	def __init__(self, socket):
		"""
		The init function is the constructor of this class.
		when the class is instantiated, it handles the instantiation of the interface class used to create sockets,
		a queue for communication between threads and instantiating the P2P object.

		Furthermore it readies the client database such that the program can write and read from it.

		args:
		- Socket : is a socket object that needs to be parsed to it.
		"""
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
		"""
		The createUser method handles the creation of the user and hashes the password before sending the create request

		args:
		- Username: The username that the user wishes to use
		- Password: The password that the user wishes to use
		"""
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
				for message in self.queue:
					if message[0] == 'createUser':
						index = self.queue.index(message)
						ret = self.queue.pop(index)
						self.event.clear()
						return ret[1]
		except:
			return False


	def login(self, username, password):
		"""
		The login method handles the login request of a user.
		It hashes the password before sending the request

		args:
		-	Username: The username of the user
		-	Password: The password of the user
		"""
		self.username = username
		self.password = password
		try:
			salt = "dinMor"
			userpassword = self.password+salt
			hashed = hashlib.md5(userpassword.encode()).hexdigest()
			sendlist = ["login",self.username,hashed]
			logindata = pickle.dumps(sendlist,pickle.HIGHEST_PROTOCOL)
			check = self.interface.send(logindata)
			event_createUser = self.event.wait(10)
			if event_createUser:
				for message in self.queue:
					if message[0] == 'login':
						self.event.clear()
						if message[1]:
							index = self.queue.index(message)
							ret = self.queue.pop(index)
							for channelname in ret[2]:
								Channel = UI_Channel_Manager(self.clientDB, channelname)
								Channel.Lookup()
							return ret[1], ret[2]
				return False
			else:
				return False
		except:
			return False


	def createChannel(self, NameOfChannel):
		"""
		The createChannel method handles the communication when creating a channel
		It creates a fernet key that is used to encrypt all messages of this channel

		Args:
		- NameOfChannel: Is the name of the channel created. This needs to be a unique name
		"""
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
					Channel.saveChannelKey()
					return ret[1]
			return False
		else:
			return False


	def joinChannel(self, NameOfChannel):
		"""
		The joinChannel method lets the user join a channel and handles the communication of this.
		Herein the method handles the usage of the P2P object and tries to receive the channel key for encryption.

		Args:
		- NameOfChannel: Is the name of an already existing channel
		"""
		try:
			sendList = ["joinChannel", NameOfChannel]
			sendList = pickle.dumps(sendList,pickle.HIGHEST_PROTOCOL)
			self.interface.send(sendList)
			event_createUser = self.event.wait(10)
			if event_createUser:
				for message in self.queue:
					if message[0] == 'joinChannel' and message[1]  == True:
						index = self.queue.index(message)
						self.queue.pop(index)
						self.event.clear()
						Key = self.P2Preceive(NameOfChannel)
						Key = pickle.loads(Key)
						Channel = UI_Channel_Manager(self.clientDB, str(NameOfChannel),Key)
						Channel.saveChannelKey()
						return True
				return False
			else:
				return False
		except Exception as e:
			print(e)
			return False
	
	def updateChannel(self, Channel):
		"""
		The updateChannel method send a request to the server that it should send the entire log of that channel.

		Args:
		-	Channel: Name of the channel that the user wants to get the channellog from
		"""
		sendList = ["chatLog", Channel]
		sendList = pickle.dumps(sendList)
		self.interface.send(sendList)
		"""
		event_update = self.event.wait(10)
		if event_update:
				for message in self.queue:
						if message[0] == 'chatLog':
								index = self.queue.index(message)
								ret = self.queue.pop(index)
								# ret = self.decrypt(ret)
								self.event.clear()
								return ret[1]
		"""

	def P2Psend(self, private, public, channel):
		"""
		P2Psend is a method used for sending a channel key via a p2p connection. It is used when receiving a p2p request from the server.

		Args:
		-	private: is the private ip address of the user trying to get the key
		-	public: is the public ip address of the user trying to get the key
		-	channel: Is the channel name of the channel that the other user is requesting the key for
		"""
		key = self.clientDB.lookup("Channel_key", channel, False)
		self.p2p.Sending(private, public, key)
		return

	def P2Preceive(self, channel):
		"""
		P2Preceive is a method used for trying to get the channel key from another user of the chat.
		It is called when a user tries to join a channel, such that they can get the channel key for encryption and decryption.

		Args:
		-	channel: Is the name of the channel that the user wants to get the channel key for.
		"""
		sendlist = ["p2p", channel]
		self.interface.send(pickle.dumps(sendlist))
		return self.p2p.Receiving()


	def sendMessage(self, message, channel):
		"""
		The sendMessage method handles the sending of messages. It uses the encryption method to encrypt the messages being send.

		Args:
		-	message: Is the message that the user wants to send. 
		-	channel: Is the name of the channel that the user wants to send the message in.
		"""
		try:
			key = self.clientDB.lookup("Channel_key", channel, False)
			message = self.encryptMessage(key, message)
			sendlist = ["logEntry", channel, message]
			sendlist = pickle.dumps(sendlist)
			check = self.interface.send(sendlist)
			return
		except:
			return False
	
	def encryptMessage(self, key, message):
		"""
		The encryptMessage method encrypt a method with a Fernet key

		Args:
		-	Key: Is the Fernet object key
		-	Message: is the message that the user wants to send
		"""		
		encMessage = key.encrypt(pickle.dumps(message))
		return encMessage
		
	def decrypt(self, ret, channel = None, Log = False):
		"""
		The decrypt method is used to decrypt a message when receiving a message from another user.

		Args:
		-	ret: Is the message that should be decrypted
		-	channel: Is the name of the channel the message belongs to.
		-	Log: Is a boolean that needs to be set to true if receiving a whole log
		"""
		if Log:
			key = self.clientDB.lookup("Channel_key", channel, False)
			ret[1] =  pickle.loads(key.decrypt(ret[1]))
			return ret
		else:
			key = self.clientDB.lookup("Channel_key", ret[0], False)
			ret[1][1] = pickle.loads(key.decrypt(ret[1][1]))
			return ret[1][1]

	def receiveMessage(self):
		"""
		The receiveMessage method handles all incoming messages and should be run on a different thread from the other methods
		It checks the request type of a messages, puts the message in a queue and sets a flag such that the other thread can handle what need to happen with the message.

		Important:
		Needs to be run on different thread such that it can listen almost all the time for messages.
		"""
		while True:
			res = self.interface.listen()
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


"""
The Channel Manager class handles channel specific things like lookup of the the key when needed and updating a specific log.
"""
class UI_Channel_Manager(UI_Session_Manager):
	
	def __init__(self,clientDB, channelName, Key=''):
		"""
		When the channel manager is initialized the constructor imports the client database into itself and sets the key and Name such that it can be used repeatedly.
		"""
		self.channelName = channelName
		self.channelKey = Key
		self.Client_DB_manager = clientDB

	def updateLog(self):
		"""
		The updateLog method is used to update the chat whenever the user logs in or that a message is sent
		"""		
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

	def saveChannelKey(self):
		"""
		The saveChannelKey method saves a channel key in a local database such that it can be retrieved when the user logs in.
		"""
		self.Client_DB_manager.createChannel(self.channelName, self.channelKey)
		with open('clientData.txt', 'wb') as bente:
			pickle.dump(self.Client_DB_manager, bente)
	
	def Lookup(self):
		"""
		The Lookup method is used to find and retrieve keys from the database.
		"""
		self.channelKey = self.Client_DB_manager.lookup(key='Channel_key',channel=self.channelName)





