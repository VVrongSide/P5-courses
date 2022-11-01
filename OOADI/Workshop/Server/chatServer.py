from DataBase.accountDB import account_DB
from DataBase.channelDB import Channel_DB
import pickle
import socket
import os.path
import threading

class chatServer(threading.Thread):
	def __init__(self):
		############ SETUP SOCKET PARAMETERS #############
		threading.Thread.__init__(self)
		self.HOST = "127.0.0.1"
		self.PORT = 65432
		# Counter for connections
		self.CONN_COUNTER = 0
		# Receive Buffer size (power of 2)    
		self.BUFFER_SIZE = 1024  
		self.MAX_SESSIONS = 5
		self.SESSION_LIST = []
		self.PORT_HANDLES = []
		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.serverSocket.bind((self.HOST, self.PORT))


		######### Initialize database files #################
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


		############ Start run method ############
		self.run()

				

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


	def getLog(self, Channel_name, lastEntry=True):
		
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

		with open(self.ChannelDB_fn, "wb") as pickle_file:
			pickle.dump(ChannelDB, pickle_file)



########## SOCKET HANDLING ###########
	def recieveData(self, datarecv):
		match datarecv[0]:
			case "login":
				return self.accountLogin(datarecv[1], datarecv[2])  ### inputs(Username, Password)
			case "createUser":
				return self.createUser(datarecv[1], datarecv[2]) ### inputs(Username, Password)
			case "joinChannel":
				return self.associateUser(datarecv[1], datarecv[2]) ### inputs(Username,Channel_name)
			case "createChannel":
				return self.createChannel(datarecv[1], datarecv[2]) ### inputs(Username, Channel_name)
			case "lastChat":
				return self.getLog(datarecv[1]) ### inputs(Channel_name)
			case "chatLog":
				return self.getLog(datarecv[1], lastEntry=False) ### input(Channel_name)
			case "logEntry":	###Input(Channel_name, msg)
				return self.logEntry(datarecv[1], datarecv[2])


	def sessionManager(self, sessionAddress, sessionSocket):
		# Recieve datalist from userSocket
		data_list = pickle.loads(sessionSocket.recv(self.BUFFER_SIZE))
		# Check if number of sessions is larger than max allowed sessions
		if len(self.SESSION_LIST)<self.MAX_SESSIONS:
			# Set session username as second entry in the unpickled object
			username=data_list[1]
			# Append username to session
			self.SESSION_LIST.append(username)

			################ TESTING PURPOSE ###################
			print('*** Connection {} accepted. Status: active/maximum sessions: {}/{}'.format(self.CONN_COUNTER,len(self.SESSION_LIST),self.MAX_SESSIONS))
			print('    from {}'.format(sessionAddress))
			print('    handled in {}'.format(threading.get_ident()))
			print('    session: {}'.format(data_list[1]))
			#####################################################
			# Create new port based on the session id/counter
			NEW_PORT=self.PORT+self.CONN_COUNTER
			print(NEW_PORT)
			# Create dedicated socket to session on the new port
			dedicatedserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			dedicatedserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			dedicatedserver.bind((self.HOST, NEW_PORT))
			# String with accepted connection
			connect_ok_list=["OK",NEW_PORT]
			data_string = pickle.dumps(connect_ok_list)
			sessionSocket.send(data_string)
			sessionSocket.close()
			print('    transferred to: {}'.format(NEW_PORT))
			# Listen for data on the dedicated socket
			dedicatedserver.listen(1)
			userHandler, userAddress = dedicatedserver.accept()
			self.PORT_HANDLES.append(userHandler)
			# Start while true loop to listen for msg on the session thread
			while True:
				recv_string = userHandler.recv(self.BUFFER_SIZE)
				recv_data = pickle.loads(recv_string)
				# If message received is "EEXIT" it should remove the connection
				if recv_data[0] == "EEXIT":
					self.SESSION_LIST.remove(username)
					print(self.SESSION_LIST)
					self.PORT_HANDLES.remove(userHandler)
					print(self.PORT_HANDLES)
					
					self.CONN_COUNTER-=1
					userHandler.close()
					print('*** Connection closed. Status: active/maximum sessions: {}/{}'.format(len(self.SESSION_LIST),self.MAX_SESSIONS))
					print('    session: {}'.format(data_list[1]))
					break
				else:
					returnVal = self.recieveData(recv_data)
					sendData = [recv_data[0], returnVal]
					userHandler.send(pickle.dumps(sendData))
		else:
			# If the connection is not successful, print the unsucessful connection
			connect_not_ok_list=["NOT OK"]
			data_string = pickle.dumps(connect_not_ok_list)
			sessionSocket.send(data_string)
			sessionSocket.close()
			print('*** Connection {} refused. Maximum numbers of sessions reached.'.format(self.CONN_COUNTER))
			print('    from {}'.format(sessionAddress))
			print('    handled in {}'.format(threading.get_ident()))
			print('    session: {}'.format(data_list[1]))

	
	################ Peer 2 Peer handling ######################
	def p2pHandler(self):



	########## RUN FUNCTION ###########
	def run(self):
		newthread = self.p2pHandler()
		newthread.start()
		while True:
			# Listen for connections on the socket
			self.serverSocket.listen(1)
			# Saves the socket and address of the session connecting
			sessionSocket, sessionAddress = self.serverSocket.accept()
			# Increment the number of connections
			self.CONN_COUNTER=self.CONN_COUNTER+1
			# Create and start new thread with a sesssion
			newthread = self.sessionManager(sessionAddress, sessionSocket)
			newthread.start()


		
if __name__=="__main__":
	
	chatserver = chatServer()
