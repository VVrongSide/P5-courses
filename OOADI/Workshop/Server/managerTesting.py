import socket
import pickle
from time import sleep
import threading

HOST = "nisker.win"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
BUFFER_SIZE = 1024 # Size of the receive buffer

class SendData(threading.Thread):
	def __init__(self,tcp_socket, user):
		threading.Thread.__init__(self)
		self.ds=tcp_socket
		self.u=user
		self.BUFFER_SIZE = 1024


	def run(self):
		while True:
			send_data = input('What to Do?: ')
			if send_data == "BYE":
				chat_data=[send_data]
				chat_string = pickle.dumps(chat_data)
				self.ds.send(chat_string)
				print("Connection closed.")
				break

			else:
				chat_data = [send_data]
			
			while True:
				send_data = input('Input your data: ')
				if send_data == "endmsg":	
					break
				
				else:
					chat_data.append(send_data)

			
			chat_string = pickle.dumps(chat_data)
			self.ds.send(chat_string)

	def addr_to_msg(self, addr):
		return '{}:{}'.format(addr[0], str(addr[1]))



class ReceiveData(threading.Thread):
	def __init__(self,tcp_socket):
		threading.Thread.__init__(self)
		self.ds = tcp_socket
		self.BUFFER_SIZE = 1024
		self.aliveRespond = ['alive']
		self.p2pSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	def run(self):
		while True:
			try:
				recv_string = self.ds.recv(BUFFER_SIZE)
				recv_data = pickle.loads(recv_string)
				if recv_data[0] == 'alive':
					self.ds.send(pickle.dumps(self.aliveRespond))
					continue

				if recv_data[0] == 'p2pRequest':
					target_priv = recv_data[1]
					target_pub = recv_data[2]
					self.p2pConnected = False
					thread1 = threading.Thread(target=self.connect, args=(target_priv, ))
					thread2 = threading.Thread(target=self.connect, args=(target_pub, ))
					thread1.start()
					thread2.start()
				
				if recv_data[0] == 'p2pAddr':
					self.p2pConnected = False
					thread1 = threading.Thread(target=self.connect, args=(1, ))
					thread2 = threading.Thread(target=self.connect, args=(2, ))
					thread1.start()
					thread2.start()

			except:
				continue
			
			print(recv_data)

	def connect(self, addr):
		self.p2pSock.connect(("nisker.win", 65433))
		local_addr = self.p2pSock.getsockname()

		print(f'connect from {local_addr} to {addr}')
		if addr == 1:
			Receive = True
			self.p2pSock.send(pickle.dumps(local_addr))
			recv_data = self.p2pSock.recv(BUFFER_SIZE)
			recv_data = pickle.loads(recv_data)
			addr = recv_data[0]

		if addr == 2:
			Receive = True
			self.p2pSock.send(pickle.dumps(local_addr))
			recv_data = self.p2pSock.recv(BUFFER_SIZE)
			recv_data = pickle.loads(recv_data)
			addr = recv_data[1]

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


		while self.p2pConnected == False:
			
			try:
				s.connect(addr)
				print("I am here")
			except:
				print("broken stuff", addr)
				break
			
			print("connected from %s to %s success!", local_addr, addr)
			

			if Receive:
				key = s.recv(1024)
				print(pickle.loads(key))
				
			else:
				key = "TestKey"
				s.send(pickle.dumps(key))

			self.p2pConnected = True
		s.close()



if __name__=="__main__":
	SESSION = input('Insert Username: ')
	print("Welcome {}. Initializing connection to the server.".format(SESSION))
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	


	thread1 = SendData(s,SESSION)
	thread2 = ReceiveData(s)
	thread1.start()
	thread2.start()
