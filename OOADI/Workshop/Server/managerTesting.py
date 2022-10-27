import socket
from socket import *
import pickle
from time import sleep
import threading

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
BUFFER_SIZE = 1024 # Size of the receive buffer

class SendData(threading.Thread):
    def __init__(self,tcp_socket, user):
        threading.Thread.__init__(self)
        self.ds=tcp_socket
        self.uu=user
    def run(self):
        print("Write text and press enter to send [EEXIT to leave chat]: ")
        while True:
            send_data = input()
            if send_data == "EEXIT":
                chat_data=[send_data]
                chat_string = pickle.dumps(chat_data)
                self.ds.send(chat_string)
                print("Connection closed.")
                break
            else:
                chat_data=[self.uu,send_data]
                chat_string = pickle.dumps(chat_data)
                self.ds.send(chat_string)
   
class ReceiveData(threading.Thread):
    def __init__(self,tcp_socket):
        threading.Thread.__init__(self)
        self.ds=tcp_socket
    def run(self):
        while True:
            recv_string =self.ds.recv(BUFFER_SIZE)
            recv_data = pickle.loads(recv_string)
            print("{}: {}".format(recv_data[0],recv_data[1]))

if __name__=="__main__":
	SESSION = 'Session_0'
	print("Welcome {}. Initializing connection to the server.".format(SESSION))
	s = socket(AF_INET,SOCK_STREAM)
	s.connect((HOST, PORT))
	connect_list=["CONNECT",SESSION]
	data_string = pickle.dumps(connect_list)
	s.send(data_string)
	data = s.recv(BUFFER_SIZE)
	data_list = pickle.loads(data)
	print("{}".format(data_list[0]))
	if data_list[0]=="OK":
		print('Reply from server: you are now connected.')
		print('You session ID is {}'.format(data_list[1]))
		print('There {} online sessions right now.'.format(data_list[2]))
		NEW_PORT=data_list[3]
		print(NEW_PORT)
		ds = socket(AF_INET,SOCK_STREAM)
		ds.connect((HOST, NEW_PORT))
		thread1 = SendData(ds,SESSION)
		thread2 = ReceiveData(ds)
		thread1.start()
		thread2.start()
	else:
		print("Reply from server: Connection is not created.")
"""
sleep(2)
tosend2 = ["login", "Gamer", "Test"]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	s.sendall(pickle.dumps(tosend2))
	recv = s.recv(1024)
	print(recv.decode()) """
