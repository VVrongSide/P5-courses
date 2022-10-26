from DataBase.accountDB import accountDB
from DataBase.channelDB import Channel_DB
import pickle
import socket
import os.path

class sessionManager:
	def __init__(self):
		self.accountDB_fn = os.path.join("DataBase","account_DB_manager.txt") 
		self.ChannelDB_fn = os.path.join("DataBase","Channel_DB_manager.txt")
		if not os.path.exists(self.accountDB_fn):
			self.accountDB = accountDB()
			with open(self.accountDB_fn, "wb") as pickle_file:
				pickle.dump(self.accountDB, pickle_file)
		if not os.path.exists(self.ChannelDB_fn):
			self.ChannelDB = Channel_DB()
			with open(self.ChannelDB_fn, "wb") as pickle_file:
				pickle.dump(self.ChannelDB, pickle_file)
			
		

#######  ACCOUNT DB HANDLING #########
	def createUser(self, Username, Password):
		with open(self.accountDB_fn, "rb") as pickle_file:
			self.accountDB = pickle.load(pickle_file)
		ret = self.accountDB.createUser(Username, Password)
		with open(self.accountDB_fn, "wb") as pickle_file:
			pickle.dump(self.accountDB, pickle_file)
		return ret
		
	def accountLogin(self, Username, Password):
		with open(self.accountDB_fn, "rb" ) as pickle_file:
			self.accountDB = pickle.load(pickle_file)
		ret = self.accountDB.logIn(Username, Password)
	
		with open(self.accountDB_fn, "wb") as pickle_file:
			pickle.dump(self.accountDB, pickle_file)
		return ret
		
	def addChannel(self, Username, Channel_name):
		with open(self.accountDB_fn, "rb" ) as pickle_file:
			self.accountDB = pickle.load(pickle_file)
		self.accountDB.addChannel(Username, Channel_name)

		with open(self.accountDB_fn, "wb") as pickle_file:
			pickle.dump(self.accountDB, pickle_file)


		
	
######### CHANNEL DB HANDLING #########
	def createChannel(self, Account, Channel_name):
		with open(self.ChannelDB_fn, "rb" ) as pickle_file:
			self.ChannelDB = pickle.load(pickle_file)
		
		ret = self.ChannelDB.createChannel(Channel_name, Account)
		
		with open(self.ChannelDB_fn, "wb" ) as pickle_file:
			pickle.dump(self.ChannelDB, pickle_file)

		if ret:
			self.addChannel(Account, Channel_name)


		return ret
		
	def associateUser(self, Account, Channel_name):
		with open(self.ChannelDB_fn, "rb") as pickle_file:
			self.ChannelDB = pickle.load(pickle_file)
		
		ret = self.ChannelDB.associateUser(Channel_name,Account)

		with open(self.ChannelDB_fn, "wb" ) as pickle_file:
			pickle.dump(self.ChannelDB, pickle_file)

		if ret:
			self.addChannel(Account, Channel_name)
		
		return ret



########## SOCKET HANDLING ###########
	def recieveData(self, datarecv):
		match datarecv[0]:
			case "login":
				self.accountLogin(datarecv[1], datarecv[2])
			case "createUser":
				self.createUser(datarecv[1], datarecv[2])
			case "joinChannel":
				self.associateUser(datarecv[1], datarecv[2])
			case "createChannel":
				self.createChannel(datarecv[1], datarecv[2])



		
if __name__=="__main__":
	HOST = "127.0.0.1"
	PORT = 65432
	session = sessionManager()
	
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		while True:
			conn, addr = s.accept()
			with conn:
				data = conn.recv(1024)
				datarecv = data
				while True:
					data = conn.recv(1024)
					if not data:
						break
					datarecv += data
				session.recieveData(pickle.loads(datarecv))



			
			