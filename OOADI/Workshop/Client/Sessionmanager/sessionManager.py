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
        self.loggedin = False
        self.interface = iSock.interface()

    def createUser(self, username, password):
        self.username = username
        self.password = password
        try:
            salt = "dinMor"
            userpassword = self.password+salt
            hashed = hashlib.md5(userpassword.encode()).hexdigest()
            sendlist = ["createUser",self.username,hashed]
            logindata = pickle.dumps(sendlist,pickle.HIGHEST_PROTOCOL)
            self.interface.send(logindata)
        except:
            return False

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
        except:
            return False

    def createChannel(self, NameOfChannel, channelPass):
        NameOfChannel = ChManager.UI_Channel_Manager(str(NameOfChannel), self.get_random_string(12))
        sendList = ["createChannel", NameOfChannel]
        sendList = pickle.dumps(sendList)
        self.interface.send(sendList)

    def joinChannel(self, NameOfChannel):
        try:
            sendList = ["joinChannel", NameOfChannel]
            sendList = pickle.dumps(sendList,pickle.HIGHEST_PROTOCOL)
            res = self.interface.send(sendList)
            if (res == True):
                return True
            else:
                return False
        except:
            return False

    def createP2PManager():
        return

    def forwardMessage(self, message, channel):
        try:
            sendlist = ["logEntry", channel, message]
            sendlist = pickle.dumps(sendlist,pickle.HIGHEST_PROTOCOL)
            check = self.interface.send(sendlist)
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

    def receiveMessage(self):
        res = self.interface.listen()
        match res[0]:
            case 'login':
                return True
            case 'createUser':
                return True
            case 'joinChannel':
                return
            case 'createChannel':
                return
            case 'lastChat':
                return
            case 'chatLog':
                return
            case 'logEntry':
                return
            

        






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
    client = UI_Session_Manager()
    client.login("mads", "dinmor")
    client.receiveMessage()





