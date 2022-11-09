import socket
import pickle
import Interface_Soket
from cryptography import fernet as f
<<<<<<< HEAD
from sessionManager import UI_Session_Manager as SM
=======
>>>>>>> main

host = "127.0.0.1"
port = 2000

#############################################################################
#
<<<<<<< HEAD
#                           Class
#
#############################################################################

class UI_Channel_Manager(SM):
=======
#                           Classes
#
#############################################################################

class UI_Channel_Manager:
>>>>>>> main
    def __init__(self, channelName, key):
        self.channelLog = []
        self.channelName = name
        self.key = f.Fernet.generate_key(key)
        self.key = Fernet(self.key)

<<<<<<< HEAD
    def sendMessage(message):
        try:
            message = super().encryptMessage(self.key, message)
            super().forwardMessage(message)
            return True
        except:
            return False
            
=======
    def sendMessage():
        return
    
>>>>>>> main
    def updateLog():
        try:
            pickledLog = Interface_Soket.interface(host, port).send(pickle.dumps(['chatlog', self.channelName]))
            self.channelLog = pickle.loads(pickledLog)
            return self.channelLog
        except:
            return False

<<<<<<< HEAD

#[[tid,navn, besked],[tid,navn,besked],[tid,navn,besked]]
=======
[[tid,navn, besked],[tid,navn,besked],[tid,navn,besked]]
>>>>>>> main



if __name__ == "__main__":
    print("Channel manager being run as main:")
    print("__________________________________")
    


