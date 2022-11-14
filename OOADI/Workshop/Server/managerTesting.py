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
					self.p2pSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
					self.p2pSock.connect(("nisker.win", 65433))
					self.p2pConnected = False
					local_addr = self.p2pSock.getsockname()
					self.p2pSock.send(pickle.dumps(local_addr))
					self.p2pSock.close()
					thread1 = threading.Thread(target=self.SendKey, args=(target_priv, local_addr ))
					thread2 = threading.Thread(target=self.SendKey, args=(target_pub, local_addr ))
					thread1.start()
					thread2.start()
				
				if recv_data[0] == 'p2pAddr':
					self.p2pSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
					self.p2pSock.connect(("nisker.win", 65433))
					self.p2pConnected = False
					thread1 = threading.Thread(target=self.ReceiveKey)
					thread1.start()

			except:
				continue
			
			print(recv_data)

	def ReceiveKey(self, first=True, addr = None):
		local_addr = self.p2pSock.getsockname()
		
		print("In receive key")
		print(local_addr)
		if first:
			self.p2pSock.send(pickle.dumps(local_addr))
			print("Sended")
			recv_data = self.p2pSock.recv(BUFFER_SIZE)
			print("Received")
			recv_list = pickle.loads(recv_data)
			addr = recv_list[0]
			print("Addr 1", addr)
			thread1 = threading.Thread(target=self.ReceiveKey, args=(False, addr, ))
			thread1.start()
			addr = recv_list[1]
			print("Addr 2", addr)
			self.p2pSock.close()
		
		
		s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s1.settimeout(2)
		s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	
		print(f'connect from {local_addr} to {addr}')
		
		while not self.p2pConnected:

			try:
				s1.connect(addr)
			except:
				#print("broken stuff", addr)
				continue
			
			print("connected from %s to %s success!", local_addr, addr)
			while True:
				try:
					print("Trying to get key")
					key = s1.recv(BUFFER_SIZE)
					print("I got the key!",pickle.loads(key))
					s1.send(pickle.dumps('23'))

					self.p2pConnected = True
					break
				except:
					print("Didn't get key")

			

			
		s1.close()


	def SendKey(self, addr, local_addr):
		
		
		s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s1.settimeout(2)
		s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

		
		print(f'connect from {local_addr} to {addr}')
		while not self.p2pConnected:
			
			try:
				s1.connect(addr)
				print("I am here")
			except:
				#print("broken stuff", addr)
				continue
			
			print("connected from %s to %s success!", local_addr, addr)
			

			key = "TestKey"
			print("Sending key:", key)
			while True:
				try:
					s1.send(pickle.dumps(key))
					print("I sent")
					recvdata = s1.recv(BUFFER_SIZE)
					print(pickle.loads(recvdata))
					break
				except:
					continue


			self.p2pConnected = True

		s1.close()




if __name__=="__main__":
	SESSION = input('Insert Username: ')
	print("Welcome {}. Initializing connection to the server.".format(SESSION))
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	


	thread1 = SendData(s,SESSION)
	thread2 = ReceiveData(s)
	thread1.start()
	thread2.start()
