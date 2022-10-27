from DataBase.accountDB import account_DB
from DataBase.channelDB import Channel_DB
import pickle
import socket
import os.path

class sessionManager:
	def __init__(self):
		self.accountDB_fn = os.path.join("DataBase","account_DB_manager.txt") 
		self.ChannelDB_fn = os.path.join("DataBase","Channel_DB_manager.txt")
		if not os.path.exists(self.accountDB_fn):
			accountDB = account_DB()
			with open(self.accountDB_fn, "wb") as pickle_file:
				pickle.dump(accountDB, pickle_file)
		if not os.path.exists(self.ChannelDB_fn):
			ChannelDB = Channel_DB()
			with open(self.ChannelDB_fn, "wb") as pickle_file:
				pickle.dump(ChannelDB, pickle_file)
		with open(self.ChannelDB_fn, "rb") as pickle_file:
			ChannelDB = pickle.load(pickle_file)
			print(ChannelDB.dictionary)

				

#######  ACCOUNT DB HANDLING #########
	def createUser(self, Username, Password):
		with open(self.accountDB_fn, "rb") as pickle_file:
			accountDB = pickle.load(pickle_file)
		ret = accountDB.createUser(Username, Password)
		with open(self.accountDB_fn, "wb") as pickle_file:
			pickle.dump(accountDB, pickle_file)
		return ret
		
	def accountLogin(self, Username, Password):
		with open(self.accountDB_fn, "rb" ) as pickle_file:
			accountDB = pickle.load(pickle_file)
		ret = accountDB.logIn(Username, Password)
	
		with open(self.accountDB_fn, "wb") as pickle_file:
			pickle.dump(accountDB, pickle_file)
		return ret
		
	def addChannel(self, Username, Channel_name):
		with open(self.accountDB_fn, "rb" ) as pickle_file:
			accountDB = pickle.load(pickle_file)
		accountDB.addChannel(Username, Channel_name)

		with open(self.accountDB_fn, "wb") as pickle_file:
			pickle.dump(accountDB, pickle_file)
	
	
######### CHANNEL DB HANDLING #########
	def createChannel(self, Account, Channel_name):
		with open(self.ChannelDB_fn, "rb" ) as pickle_file:
			ChannelDB = pickle.load(pickle_file)
		
		ret = ChannelDB.createChannel(Channel_name, Account)
		
		with open(self.ChannelDB_fn, "wb" ) as pickle_file:
			pickle.dump(ChannelDB, pickle_file)

		if ret:
			self.addChannel(Account, Channel_name)


		return ret
		
	def associateUser(self, Account, Channel_name):
		with open(self.ChannelDB_fn, "rb") as pickle_file:
			ChannelDB = pickle.load(pickle_file)
		
		ret = ChannelDB.associateUser(Channel_name,Account)

		with open(self.ChannelDB_fn, "wb" ) as pickle_file:
			pickle.dump(ChannelDB, pickle_file)

		if ret:
			self.addChannel(Account, Channel_name)
		return ret


	def getLogs(self, Channel_name, lastEntry=True):
		
		with open(self.ChannelDB_fn, "rb") as pickle_file:
			ChannelDB = pickle.load(pickle_file)

		if lastEntry:
			return ChannelDB.lookup(ChannelDB.columns[2], Channel_name)
		else: 
			return ChannelDB.lookup(ChannelDB.columns[2], Channel_name, False)


	def getMembers(self, Channel_name):
		with open(self.ChannelDB_fn, "rb") as pickle_file:
			ChannelDB = pickle.load(pickle_file)
		
		return ChannelDB.lookup(ChannelDB.columns[1], Channel_name, False)


	def logEntry(self, Channel_name, msg):
		with open(self.ChannelDB_fn, "rb") as pickle_file:
			ChannelDB = pickle.load(pickle_file)
		
		ChannelDB.logEntry(Channel_name, msg)

		with open(self.ChannelDB_fn, "wb") as picklefile:
			pickle.dump(ChannelDB, pickle_file)



########## SOCKET HANDLING ###########
	def recieveData(self, datarecv):
		match datarecv[0]:
			case "login":
				return self.accountLogin(datarecv[1], datarecv[2])
			case "createUser":
				return self.createUser(datarecv[1], datarecv[2])
			case "joinChannel":
				return self.associateUser(datarecv[1], datarecv[2])
			case "createChannel":
				return self.createChannel(datarecv[1], datarecv[2])
			case "lastChat":
				return self.getLogs(datarecv[1])
			case "chatLogs":
				return self.getLogs(datarecv[1], lastEntry=False)




		
if __name__=="__main__":
	HOST = "127.0.0.1"
	PORT = 65432
	session = sessionManager()
	
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		while True:
			print("Here")
			conn, addr = s.accept()
			with conn:
				datarecv = conn.recv(1024)
				while True:
					data = conn.recv(1024)
					if not data:
						break
					datarecv += data
				ret = session.recieveData(pickle.loads(datarecv))
				if type(ret) is bool:
					conn.sendall(pickle.dumps(ret))
				elif type(ret) is list:
					conn.sendall(pickle.dumps(ret))
				print(ret)
				
				



			
			