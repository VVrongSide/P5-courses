import socket
import pickle
import hashlib
import Interface_Soket as iSock
import threading
from cryptography import fernet as f
from clientDB import Client_DB
import os
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
		try:
			salt = "dinMor"
			saltypassword = password+salt
			hashed = hashlib.md5(saltypassword.encode()).hexdigest()
			sendlist = ["createUser",username,hashed]
			logindata = pickle.dumps(sendlist)
			self.interface.send(logindata)

			event = self.event.wait(10)
			if event:
				for message in self.queue:
					if message[0] == 'createUser':
						index = self.queue.index(message)
						ret = self.queue.pop(index)
						self.event.clear()
						print("Popped: ",ret, "\n")
						return ret[1]
		except:
			return False
		return False

	def login(self, username, password):
		try:
			salt = "dinMor"
			saltypassword = password+salt
			hashed = hashlib.md5(saltypassword.encode()).hexdigest()
			sendlist = ["login",username,hashed]
			logindata = pickle.dumps(sendlist)
			self.interface.send(logindata)
			event = self.event.wait(10)
			if event:
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
		except:
			pass
		return False

	def createChannel(self, NameOfChannel):
		sendList = ["createChannel", NameOfChannel]
		sendList = pickle.dumps(sendList)
		self.interface.send(sendList)

		event = self.event.wait(10)
		if event:
			self.event.clear()
			for message in self.queue:
				if message[0] == 'createChannel' and message[1] == True:
					index = self.queue.index(message)
					ret = self.queue.pop(index)
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
			sendList = pickle.dumps(sendList,pickle)
			self.interface.send(sendList)
			event = self.event.wait(10)
			if event:
				for message in self.queue:
					if message[0] == 'joinChannel' and message[1]  == True:
						index = self.queue.index(message)
						self.queue.pop(index)
						self.event.clear()

						print("p2p: før \n")  # Print til troubleshoot
						
						while True:
							try:
								Key = self.P2Preceive(NameOfChannel)
								if Key == None:
									raise Exception
								Key = pickle.loads(Key)
								break
							except Exception as e:
								print(e)
								continue

						print("p2p: efter \n") # Samme her
						Channel = UI_Channel_Manager(self.clientDB, str(NameOfChannel),Key)
						Channel.Howtosavealife()
						return True
				return False
			else:
				return False
		except Exception as e:
			print(e)
			return False

	def updateChannel(self, Channel):
		sendList = ["chatLog", Channel]
		sendList = pickle.dumps(sendList)
		self.interface.send(sendList)
		

	def P2Psend(self, private, public, channel):
		key = self.clientDB.lookup("Channel_key", channel, False)
		print("Starter p2p class function for sending \n")
		self.p2p.Sending(private, public, key)
		return

	def P2Preceive(self, channel):
		sendlist = ["p2p", channel]
		self.interface.send(pickle.dumps(sendlist))
		print("Starter p2p class function for receiving \n")
		return self.p2p.Receiving()


	def sendMessage(self, message, channel):
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
		encMessage = key.encrypt(pickle.dumps(message))
		return encMessage


	def decrypt(self, ret):
		key = self.clientDB.lookup("Channel_key", ret[0], False)
		ret[1][1] = pickle.loads(key.decrypt(ret[1][1]))
		return ret[1][1]


	def receiveMessage(self):
		while True:
			res = self.interface.listen()
			print("Receive function: \n",res, "\n")
			match res[0]:
				case 'login':
					if (res[1] == False):
						self.loggedin = False
						self.event.set()
					else:
						self.queue.append(res)
						self.event.set()

				case 'createUser':
					if (res[1] == False):
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





