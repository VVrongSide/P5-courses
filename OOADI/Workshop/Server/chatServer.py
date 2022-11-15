import sys
from time import sleep
from DataBase.accountDB import account_DB
from DataBase.channelDB import Channel_DB
import pickle
import socket
import os.path
import threading

class chatServer(threading.Thread):
	def __init__(self):
		############ SETUP SOCKET PARAMETERS #############
		super().__init__()
		self.PORT = 65432
		self.p2pPort = 65433
		
		# Receive Buffer size (must be a power of 2)
		self.BUFFER_SIZE = 1024

		# Bind the socket without specifying host address to work with all host addresses
		self.serverSocket = socket.socket()
		self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.serverSocket.bind(("", self.PORT))

		# Bind p2p Socket
		self.p2pSocket = socket.socket()
		self.p2pSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.p2pSocket.bind(("",self.p2pPort))

		# Create dictionary and list with online user information
		self.onlineUsers = {
			"ipAddress" : [],
			"Username" : []
			}
		self.connections = []		

		# Define the default alive Check message
		self.aliveCheck = ['alive']


		######### Initialize database files #################
		# Define the paths for where the pickled DB files are
		self.accountDB_fn = os.path.join("DataBase","account_DB_manager.txt") 
		self.ChannelDB_fn = os.path.join("DataBase","Channel_DB_manager.txt")

		# If the DB files are yet to be created, create them:
		if not os.path.exists(self.accountDB_fn):
			accountDB = account_DB()
			with open(self.accountDB_fn, "wb") as pickle_file:
				pickle.dump(accountDB, pickle_file)
		if not os.path.exists(self.ChannelDB_fn):
			ChannelDB = Channel_DB()
			with open(self.ChannelDB_fn, "wb") as pickle_file:
				pickle.dump(ChannelDB, pickle_file)

		############ Start run method ############
		self.run()

	########### Pop user from the onlineUsers dictionary ###############
	def userPop(self,ipaddress):
		userIndex = self.onlineUsers["ipAddress"].index(ipaddress)
		self.onlineUsers["ipAddress"].pop(userIndex)
		self.onlineUsers["Username"].pop(userIndex)
		self.connections.pop(userIndex)
		print(self.onlineUsers)
		print(f'Open conncetions: {len(self.connections)}')


#######################################	
######### ACCOUNT DB HANDLING #########
#######################################	


	############# Create a user in the accountDB ##########
	def createUser(self, Username, Password, userIndex):
		# Load the pickled account object
		with open(self.accountDB_fn, "rb") as pickle_file:
			accountDB = pickle.load(pickle_file)
		ret = accountDB.createUser(Username, Password)

		# If account was succesfully created, write the modified DB to the pickled file
		if ret:
			with open(self.accountDB_fn, "wb") as pickle_file:
				pickle.dump(accountDB, pickle_file)
			self.onlineUsers["Username"][userIndex] = Username
			print(self.onlineUsers)
		return ret
		

	########### Check the username and password in the accountDB #########
	def accountLogin(self, Username, Password, userIndex):
		# Load the pickled account object
		with open(self.accountDB_fn, "rb" ) as pickle_file:
			accountDB = pickle.load(pickle_file)
		ret = accountDB.logIn(Username, Password)

		if ret:
			self.onlineUsers["Username"][userIndex] = Username
			print(self.onlineUsers)
			return [ret, accountDB.memberOfChannels(Username)]

		# Return whether the login was succesful or not
		return ret
		
	
	########### associate a channel with a user in the accountDB ###########
	def addChannel(self, Username, Channel_name):
		# Load the pickled acconut object
		with open(self.accountDB_fn, "rb" ) as pickle_file:
			accountDB = pickle.load(pickle_file)
		
		# Call the accountDB addChannel method
		accountDB.addChannel(Username, Channel_name)

		# Write the modified accountDB object to a pickled file
		with open(self.accountDB_fn, "wb") as pickle_file:
			pickle.dump(accountDB, pickle_file)
	
#######################################	
######### CHANNEL DB HANDLING #########
#######################################


######### Creation of Channel #########
	def createChannel(self, Account, Channel_name):
		# Load the pickled object
		with open(self.ChannelDB_fn, "rb" ) as pickle_file:
			ChannelDB = pickle.load(pickle_file)
		
		# Use the DB createChannel method
		ret = ChannelDB.createChannel(Channel_name, Account)
		
		# If succesful in creation of channel:
		if ret:
			# Write the changed object to pickled file
			with open(self.ChannelDB_fn, "wb" ) as pickle_file:
				pickle.dump(ChannelDB, pickle_file)
			self.addChannel(Account, Channel_name)
			

		# If unsuccesful will return false
		return ret
		

########### Associate user with channel ###########
	def associateUser(self, Account, Channel_name):

		# Load the pickled object
		with open(self.ChannelDB_fn, "rb") as pickle_file:
			ChannelDB = pickle.load(pickle_file)


		ret = ChannelDB.associateUser(Channel_name,Account)

		# If associate user was succesful proceed to pickle the modified ChannelDB object
		if ret:
			with open(self.ChannelDB_fn, "wb" ) as pickle_file:
				pickle.dump(ChannelDB, pickle_file)
			self.addChannel(Account, Channel_name)

		
		return ret




########## Get chatlog from channel ###############
	def getLog(self, Channel_name, lastEntry=True):

		# Load the Pickled channelDB object		
		with open(self.ChannelDB_fn, "rb") as pickle_file:
			ChannelDB = pickle.load(pickle_file)

		# If lastentry is true, will only return the last message in the chatlog
		if lastEntry:
			return ChannelDB.lookup(ChannelDB.columns[2], Channel_name)
		# Else return the entire chat log for the channel
		else: 
			return ChannelDB.lookup(ChannelDB.columns[2], Channel_name, False)


########## Get member list of channel #############
	def getMembers(self, Channel_name):
		# Load the pickled channelDB object
		with open(self.ChannelDB_fn, "rb") as pickle_file:
			ChannelDB = pickle.load(pickle_file)
		
		# Return the member list
		return ChannelDB.lookup(ChannelDB.columns[1], Channel_name, False)


########### Write an entry in a chatlog ###########
	def logEntry(self, Channel_name, msg):
		# Load the pickled channelDB object
		with open(self.ChannelDB_fn, "rb") as pickle_file:
			ChannelDB = pickle.load(pickle_file)
		
		# Add the entry using the logEntry method from the channelDB
		ChannelDB.logEntry(Channel_name, msg)

		# Write the modified channel object to a pickled file
		with open(self.ChannelDB_fn, "wb") as pickle_file:
			pickle.dump(ChannelDB, pickle_file)

		members = self.getMembers(Channel_name)
		sendmsg = ['logEntry', msg]
		for i in members:
			print(i)
			if i in self.onlineUsers["Username"]:
				print(i)
				connIndex = self.onlineUsers["Username"].index(i)
				self.connections[connIndex][0].send(pickle.dumps(sendmsg))
		




########## SOCKET HANDLING ###########
	def recieveData(self, datarecv, ipaddress):
		# Match - Case for recieving data
		userIndex = self.onlineUsers["ipAddress"].index(ipaddress)
		username = self.onlineUsers["Username"][userIndex]
		try:
			match datarecv[0]:
				case "login":
					return [self.accountLogin(datarecv[1], datarecv[2],userIndex)]  ### inputs(Username, Password, userIndex)
				case "createUser":
					return [self.createUser(datarecv[1], datarecv[2], userIndex)] ### inputs(Username, Password)
				case "joinChannel":
					return [self.associateUser(username, datarecv[1])] ### inputs(Username,Channel_name)
				case "createChannel":
					return [self.createChannel(username, datarecv[1])] ### inputs(Username, Channel_name)
				case "lastChat":
					return [self.getLog(datarecv[1])] ### inputs(Channel_name)
				case "chatLog":
					return [self.getLog(datarecv[1], lastEntry=False)] ### input(Channel_name)
				case "logEntry":
					return [self.logEntry(datarecv[1], datarecv[2])] ###Input(Channel_name, msg)
				case _:
					return ["Invalid request type"]
		except:
			return False


############## Handles the individual connections with clients (Started as thread for single client) ##################
	def clientHandler(self, connection, ipaddress):
		#connection.send(str.encode('You are now connected to the replay server... Type BYE to stop'))
		connection.settimeout(10)
		# Loop which keeps listening on the connection untill a BYE signal is recieved
		while True:
			try:
				recv_string = connection.recv(self.BUFFER_SIZE)
				if not recv_string:
					break
				recv_data = pickle.loads(recv_string)
				clientIndex = self.onlineUsers["ipAddress"].index(ipaddress)
			except:
				# If alivecheck has been sent and nothing was received (timeout) break loop and close connection
				clientIndex = self.onlineUsers["ipAddress"].index(ipaddress)
				if self.connections[clientIndex][1] == 0:
					break
				continue

			# If the alivecheck has been sent and a alive was received, tell this to shared variable.
			if recv_data[0] == 'alive':
				self.connections[clientIndex][1] = 1
				continue

			if recv_data[0] == 'p2p':
				tp = threading.Thread(target=self.p2pHandler, args=(recv_data[1], self.onlineUsers["Username"][clientIndex], ))
				tp.start()
				sendData = ['p2pAddr']
				connection.sendall(pickle.dumps(sendData))
				sleep(2)
				continue

			
			# If bye signal was sent from client, break loop and close connection
			if recv_data[0] == 'BYE':
				break
			

			returnVal = self.recieveData(recv_data,ipaddress)
			
			if recv_data[0] == 'logEntry':
				continue

			sendData = [recv_data[0]]
			sendData.append(returnVal)
			
			connection.sendall(pickle.dumps(sendData))
			
		
		# When BYE is recieved close the connection
		self.userPop(ipaddress)
		connection.close()
		sys.exit()


###################### CHECK CONNECTION STATUS ############################
	def aliveChecker(self):
		while True:
			# Iterate through the know ipAddresses
			for addr in self.onlineUsers["ipAddress"]:
				# Get index of ipAddress
				connIndex = self.onlineUsers["ipAddress"].index(addr)

				# Check the alive status of the connection
				if self.connections[connIndex][1] == 1:

					try:
						# Send alive ping
						self.connections[connIndex][0].send(pickle.dumps(self.aliveCheck))
						# Set alive status to 0 to indicate an alivecheck has been sent
						self.connections[connIndex][1] = 0
					except socket.timeout:
						# Set alive status to 0 in case of timeout, since this means no connection to user
						self.connections[connIndex][1] = 0
				sleep(1)



################### Peer 2 Peer handling ######################
	
	def p2pHandler(self, Channel_name, Username):
		members = self.getMembers(Channel_name)
		self.p2pSocket.listen()
		p2pSocket1, p2pAddress1 = self.p2pSocket.accept()
		p2pClient = [[p2pSocket1, p2pAddress1]]

		recv_data = p2pSocket1.recv(self.BUFFER_SIZE)
		p2pClient[0].append(pickle.loads(recv_data))
		#print(p2pClient)

		print('The current members are:', members)

		for member in members:
			if member != Username:
				print('Trying to reach member:', member)
				if member in self.onlineUsers["Username"]:
					
					# Connect to member already in channel
					senddata = ["p2pRequest", p2pClient[0][1], p2pClient[0][2]]
					print("Sending data to sender:", senddata)
					index = self.onlineUsers["Username"].index(member)
					self.connections[index][0].send(pickle.dumps(senddata))
					
					print("The current connections are: \n", self.connections[index], "\n")
					
					# Get info from already connected user
					p2pSocket2, p2pAddress2 = self.p2pSocket.accept()
					p2pClient.append([p2pSocket2, p2pAddress2])
					recvdata = p2pClient[1][0].recv(self.BUFFER_SIZE)
					priv_addr = pickle.loads(recvdata)
					pub_addr = p2pClient[1][1]

					# Send info to user who wants to join
					sendData = [priv_addr, pub_addr]
					print('Sending data to receiver: ', sendData)
					p2pClient[0][0].send(pickle.dumps(sendData))
					print("Sent data to receiver, closing thread")
					break
		
		p2pClient[0][0].close()
		p2pClient[1][0].close()
		sys.exit()
		



					



	########## RUN FUNCTION ###########
	def run(self):
		# Listen for connections on the socket
		self.serverSocket.listen(1)
		#t = threading.Thread(target=self.aliveChecker)
		#t.start()
		while True:
			# Accept new connections to the server
			sessionSocket, sessionAddress = self.serverSocket.accept()
			print(f'Connection from: ({sessionAddress[0]}:{sessionAddress[1]})')
			self.onlineUsers["ipAddress"].append(sessionAddress)
			self.onlineUsers["Username"].append(None)
			self.connections.append([sessionSocket,1])
			print(f'Open connections: {len(self.connections)}')
			# Create and start new thread which handles the new connection
			t = threading.Thread(target=self.clientHandler, args=(sessionSocket, sessionAddress, ))
			t.start()
		
		
if __name__=="__main__":
	# Initiate the class
	chatserver = chatServer()


