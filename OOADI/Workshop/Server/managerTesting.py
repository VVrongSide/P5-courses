import socket
import pickle
from time import sleep

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server


tosend = ["lastChat", ""]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	s.sendall(pickle.dumps(tosend))
	datarecv = s.recv(1024)
	while True:
		data = s.recv(1024)
		if not data:
			break
		datarecv += data
	print(datarecv.decode())


"""
sleep(2)
tosend2 = ["login", "Gamer", "Test"]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	s.sendall(pickle.dumps(tosend2))
	recv = s.recv(1024)
	print(recv.decode()) """
