import socket
import pickle
import hashlib
import Interface_Soket as iSock
import cryptography
import channel_Manager as ChManager
import random
import string
import threading

#############################################################################
#
#                           Class
#
#############################################################################

class UI_Session_Manager(threading.Thread):
    def __init__(self):
        self.loggedin = False
        self.interface = iSock.interface()
        self.Channels = []

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
            self.interface.send(sendList)
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
                if (res[1] == True):
                    self.password = ""
                    self.username = ""
                    self.loggedin = False
                    return false
                else:
                    return True

            case 'createUser':
                if (res[1] == False):
                    self.username = ""
                    self.password = ""
                    return False
                else:
                    self.loggedin = True
                    return True

            case 'joinChannel':
                if (res[1] == False):
                    return False
                else:
                        
                    return 'joinChannel', True

            case 'createChannel':
                return True

            case 'lastChat':
                lastMessage = res[1]
                return lastMessage

            case 'chatLog':
                return res[2]

            case other:
                return False
            

        






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





