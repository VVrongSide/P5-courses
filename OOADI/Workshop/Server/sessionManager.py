from DataBase.accountDB import accountDB
import pickle
import socket
import os.path

class sessionManager:
	def __init__(self):
		self.accountDB_fn = os.path.join("DataBase","Channel_DB_manager.txt") 
		self.ChannelDB_fn = os.path.join("DataBase","Channel_DB_manager.txt")
		if not self.filename.exists():
			self.accountDataB = accountDB()
			with open(self.accountDB_fn, "wb") as pickle_file:
				pickle.dump(self.accountDataB, pickle_file)
		


	def createUser(self, Username, Password):
		with open(self.accountDB_fn, "rb") as pickle_file:
			self.accountDataB = pickle.load(pickle_file)
		if self.accountDataB.createUser(Username, Password):
			with open(self.accountDB_fn, "wb") as pickle_file:
				pickle.dump(self.accountDataB, pickle_file)
			return True
		else:
			with open(self.accountDB_fn, "wb") as pickle_file:
				pickle.dump(self.accountDataB, pickle_file)
			return False

	def accountLogin(self, Username, Password):
		with open(self.accountDB_fn, "wb" ) as pickle_file:
			self.accountDataB = pickle.load(pickle_file)
		if self.accountDataB.logIn(Username, Password):
			with open(self.accountDB_fn, "wb") as pickle_file:
				pickle.dump(self.accountDataB, pickle_file)
			return True
		else:
			with open(self.accountDB_fn, "wb") as pickle_file:
				pickle.dump(self.accountDataB, pickle_file)
			return False

	def recieveData(self, datarecv):
		msgType = list(datarecv.split(" "))
		match msgType[0]:
			case "login":
				self.accountLogin(msgType[1], msgType[2])
			case "createUser":
				self.createUser(msgType[1], msgType[2])



		
if __name__=="__main__":
	HOST = "127.0.0.1"
	PORT = 80
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		conn, addr = s.accept()
		with conn:
			datarecv = ""
			while True:
				data = conn.recv(1024)
				if not data:
					break
				datarecv += data.decode('utf8')
			