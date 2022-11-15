import socket
import pickle
import sys
import threading



class p2pClass:
	def __init__(self):
		self.HOST = "nisker.win"
		self.PORT = 65433
		self.BUFFER_SIZE = 1024


	def Receiving(self):
		self.p2pSock = self.sockSetup()
		self.p2pSock.connect(("nisker.win", 65433))
		self.p2pConnected = False
		local_addr = self.p2pSock.getsockname()
		self.p2pSock.send(pickle.dumps(local_addr))
		recv_data = self.p2pSock.recv(self.BUFFER_SIZE)
		recv_data = pickle.loads(recv_data)
		priv_addr = recv_data[0]
		pub_addr = recv_data[1]
		thread1 = threading.Thread(target=self.ReceiveKey, args=(priv_addr, local_addr, ))
		thread1.start()
		thread2 = threading.Thread(target=self.ReceiveKey, args=(pub_addr, local_addr, ))
		thread2.start()
		self.p2pSock.close()




	def Sending(self, target_priv, target_pub):
		self.p2pSock = self.sockSetup()
		self.p2pSock.connect(("nisker.win", 65433))
		self.p2pConnected = False
		local_addr = self.p2pSock.getsockname()
		self.p2pSock.send(pickle.dumps(local_addr))
		self.p2pSock.close()
		thread1 = threading.Thread(target=self.SendKey, args=(target_priv, local_addr ))
		thread2 = threading.Thread(target=self.SendKey, args=(target_pub, local_addr ))
		thread1.start()
		thread2.start()



	def ReceiveKey(self, addr = None, local_addr=None):

		s1 = self.sockSetup()
		s1.bind(local_addr)
		

		print(f'Trying to connect from {local_addr} to {addr}')
		thisAddr = False

		# If not connected try connecting
		while not self.p2pConnected:
			try:
				s1.connect(addr)
				thisAddr = True
				self.p2pConnected = True
			except:
				continue
			print(f'connected from {local_addr} to {addr} success!')

		# Try to receive on the connected address
		if thisAddr:
			while True:
				try:
					print("Trying to get key")
					key = s1.recv(self.BUFFER_SIZE)
					print("I got the key!: ",pickle.loads(key))
					s1.send(pickle.dumps('Succesfully received'))
					break
				except:
					continue

		# Close socket and exit thread
		s1.close()
		sys.exit()

	def SendKey(self, addr, local_addr, key):
		
		# Set up the socket for connecting to a user
		s1 = self.sockSetup()
		s1.bind(local_addr)
		
		
		print(f'Trying to connect from {local_addr} to {addr}')
		thisAddr = False
		# While not connected to a p2p address try:
		while not self.p2pConnected:
			
			try:
				s1.connect(addr)
				thisAddr = True
				self.p2pConnected = True
			except:
				continue
			print(f'connected from {local_addr} to {addr} success!')
			

		# If connected to an address:
		if thisAddr:
			print("Sending key:", key)
			while True:
				try:
					s1.send(pickle.dumps(key))
					print("I sent")
					recvdata = s1.recv(self.BUFFER_SIZE)
					print(pickle.loads(recvdata))
					break
				except:
					continue
		# Close socket and exit thread
		s1.close()
		sys.exit()


	def sockSetup(self):
		s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s1.settimeout(2)
		s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		return s1
