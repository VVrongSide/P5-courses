import socket, threading

HOST = ''           # Symbolic name meaning all available interfaces
PORT = 8888         # Arbitrary non-privileged port
CONN_COUNTER = 0    # Counter for connections
BUFFER_SIZE = 1024  # Receive Buffer size (power of 2)

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket,cc):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.counter = cc
    def run(self):
        r = self.csocket.recv(BUFFER_SIZE)
        print('*** Connection {}'.format(self.counter))
        print('    from {}'.format(clientAddress))
        print('    handled in {}'.format(threading.get_ident()))
        print('    incoming text: {}'.format(r))
        self.csocket.send(bytes('Hi there! Got your message from {}'.format(clientAddress[0]),'utf-8'))
        self.csocket.close()
        print('    connection closed')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    CONN_COUNTER = CONN_COUNTER + 1
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock, CONN_COUNTER)
    newthread.start()
    
