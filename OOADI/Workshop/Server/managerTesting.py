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
		self.aliveCheck = ['alive', True]
	def run(self):
		while True:
			recv_string = self.ds.recv(BUFFER_SIZE)
			recv_data = pickle.loads(recv_string)
			
			if recv_data[0] != 'alive':	
				if type(recv_data[0]) == bool:
					if recv_data[0]:
						print("Success")
					else:
						print("Failure")
				else:
					print(recv_data)
				continue
			print(recv_data)
			self.ds.send(pickle.dumps(self.aliveCheck))



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
