import socket
from socket import *
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
					if chat_data[0] == 'p2p':
						chat_data.append(self.ds.gethostname)

					break
				else:
					chat_data.append(send_data)

			
			chat_string = pickle.dumps(chat_data)
			self.ds.send(chat_string)


class ReceiveData(threading.Thread):
	def __init__(self,tcp_socket):
		threading.Thread.__init__(self)
		self.ds = tcp_socket
		self.BUFFER_SIZE = 1024
		self.aliveRespond = ['alive']
		self.priv_addr = self.ds.gethostname
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

					thread1 = threading.Thread(target=self.connect, args=(self.priv_addr, target_priv, recv_data[3]))
					thread2 = threading.Thread(target=self.connect, args=(self.priv_addr, target_pub, recv_data[3]))
					thread1.start()
					thread2.start()


				if recv_data[0] == 'p2pAddr':
					target_priv = recv_data[1]
					target_pub = recv_data[2]
					thread1 = threading.Thread(target=self.connect, args=(self.priv_addr, target_priv, recv_data[3]))
					thread2 = threading.Thread(target=self.connect, args=(self.priv_addr, target_pub, recv_data[3]))
					thread1.start()
					thread2.start()

			except:
				continue
			
			print(recv_data)

	def connect(self, local_addr, addr, Recieve = True):
		print("connect from %s to %s", local_addr, addr)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(2)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		s.bind(local_addr)
		while self.p2pConnected == False:
			try:
				s.connect(addr)
			except socket.error:
				pass
			print("connected from %s to %s success!", local_addr, addr)
			if Recieve:
				key = s.recv(1024)
				print(pickle.loads(key))
			else:
				key = "TestKey"
				sendAddr = [local_addr]
				self.ds.send(pickle.dumps(sendAddr))
				sendkey = pickle.dumps(key)
				s.send(sendkey)

			self.p2pConnected = True

		s.close()



if __name__=="__main__":
	SESSION = input('Insert Username: ')
	print("Welcome {}. Initializing connection to the server.".format(SESSION))
	s = socket(AF_INET,SOCK_STREAM)
	s.connect((HOST, PORT))
	#recv_string = s.recv(BUFFER_SIZE)
	#print(recv_string.decode('utf-8'))
	thread1 = SendData(s,SESSION)
	thread2 = ReceiveData(s)
	thread1.start()
	thread2.start()
