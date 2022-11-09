import socket
import pickle
import hashlib
import Interface_Soket as iSock
import cryptography
import channel_Manager as ChManager
import random
import string

#############################################################################
#
#                           Class
#
#############################################################################

class UI_Session_Manager:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = port
        self.loggedin = False
        self.interface = iSock.interface(self.host, self.port)

    def login(self, username, password):
        self.username = username
        self.password = password
        try:
            salt = "dinMor"
            userpassword = self.password+salt
            hashed = hashlib.md5(userpassword.encode()).hexdigest()
            sendlist = ["login",self.username,hashed]
            logindata = pickle.dumps(sendlist,pickle.HIGHEST_PROTOCOL)
            self.interface.send(logindata)
            return True
        except:
            return False

    def createChannelManager(NameOfChannel):
        NameOfChannel = ChManager.UI_Channel_Manager(channelName, self.get_random_string(12))
        return NameOfChannel

    def createP2PManager():
        return

    def forwardMessage(self, message):
        try:
            sendlist = ["tid", self.username, message]
            sendlist = pickle.dumps(sendlist,pickle.HIGHEST_PROTOCOL)
            self.interface.send(sendlist)
            return True
        except:
            return False
    
    def logout():
        del self

    def encryptMessage(key, message):
        encMessage = key.encrypt(message)
        return encMessage
        
    def decrypt(key, encmessage):
        message = key.decrypt(encmessage)
        return message

    def get_random_string(length):
        # choose from all lowercase letter
        letters = string.printable
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def __delete__():
        print("Deleted session")





#############################################################################
#
#                           Initial test things
#
#############################################################################

class connectionSocket:
    def __init__(self, port):
        self.port = port
        self.host = "127.0.0.1"


    def echo(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(b"Hello, world")
            data = s.recv(1024)
        print(f"Received {data!r}")

#############################################################################
#
#                           Execution if main
#
#############################################################################

if __name__ == "__main__":
    client = UI_Session_Manager("Hejdu", "1234567", 2000)
    client.login()




