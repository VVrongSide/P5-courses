from DataBase.accountDB import account_DB
from DataBase.channelDB import Channel_DB
import pickle
import socket
import os.path
import threading

class sessionManager(threading.Thread):
	def __init__(self,sessionAddress,sessionSocket,cc,uu,ii,pi,hi):
		threading.Thread.__init__(self)
		self.csocket = sessionSocket
		self.counter = cc
		self.sesessions = uu
		self.sessionIDs = ii
		self.portids = pi
		self.porthandles = hi
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
			#print(ChannelDB.dictionary)

				

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

########## RUN FUNCTION ###########
	def run(self):
		r = self.csocket.recv(BUFFER_SIZE)
		data_list = pickle.loads(r)
		if len(self.sesessions)<MAX_SESSIONS:
			indid=self.counter
			self.sessionIDs.append(indid)
			uusername=data_list[1]
			self.sesessions.append(uusername)
			print('*** Connection {} accepted. Status: active/maximum sessions: {}/{}'.format(self.counter,len(self.sesessions),MAX_SESSIONS))
			print('    from {}'.format(sessionAddress))
			print('    handled in {}'.format(threading.get_ident()))
			print('    session: {}'.format(data_list[1]))
			onlineusers=len(self.sessionIDs)
			NEW_PORT=PORT+self.counter
			print(NEW_PORT)
			self.portids.append(NEW_PORT)
			dedicatedserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			dedicatedserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			dedicatedserver.bind((HOST, NEW_PORT))
			connect_ok_list=["OK",indid,onlineusers,NEW_PORT]
			data_string = pickle.dumps(connect_ok_list)
			self.csocket.send(data_string)
			self.csocket.close()
			print('    transferred to: {}'.format(NEW_PORT))
			dedicatedserver.listen(1)
			ds, userAddress = dedicatedserver.accept()
			self.porthandles.append(ds)
			while True:
				recv_string =ds.recv(BUFFER_SIZE)
				recv_data = pickle.loads(recv_string)
				if recv_data[0] == "EEXIT":
					self.sesessions.remove(uusername)
					print(self.sesessions)
					self.portids.remove(NEW_PORT)
					print(self.portids)
					self.porthandles.remove(ds)
					print(self.porthandles)
					self.sessionIDs.remove(indid)
					print(self.sessionIDs)
					self.counter=self.counter-1
					ds.close()
					print('*** Connection closed. Status: active/maximum sessions: {}/{}'.format(len(self.sesessions),MAX_SESSIONS))
					print('    session: {}'.format(data_list[1]))
					break
				else:
					for x in self.porthandles:
						if x != ds:
							x.send(recv_string)
						else:
							print("Message received from {}: {}".format(recv_data[0],recv_data[1]))
		else:
			connect_not_ok_list=["NOT OK"]
			data_string = pickle.dumps(connect_not_ok_list)
			self.csocket.send(data_string)
			self.csocket.close()
			print('*** Connection {} refused. Maximum numbers of sessionss reached.'.format(self.counter))
			print('    from {}'.format(sessionAddress))
			print('    handled in {}'.format(threading.get_ident()))
			print('    session: {}'.format(data_list[1]))

		
if __name__=="__main__":
	HOST = "127.0.0.1"
	PORT = 65432
	CONN_COUNTER = 0    # Counter for connections
	BUFFER_SIZE = 1024  # Receive Buffer size (power of 2)
	MAX_SESSIONS = 5
	SESSION_LIST = []
	ID_LIST = []
	PORT_IDS = []
	PORT_HANDLES = []
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.bind((HOST, PORT))
	print("SessionManager started.")
	print("Waiting for session connections...")
	while True:
		server.listen(1)
		sessionSocket, sessionAddress = server.accept()
		CONN_COUNTER=CONN_COUNTER+1
		newthread = sessionManager(sessionAddress, sessionSocket, CONN_COUNTER, SESSION_LIST, ID_LIST, PORT_IDS, PORT_HANDLES)
		newthread.start()
	"""
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
	"""	