from socket import *
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8888
BUFFER_SIZE = 1024

s = socket(AF_INET,SOCK_STREAM)
s.connect((SERVER_IP, SERVER_PORT))

print('Blocking server....')
timeVar=0;
while True:
    time.sleep(5)
    timeVar=timeVar+5
    print('I have been blocking the server for {} seconds'.format(timeVar))

