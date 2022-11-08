import socket
import pickle
import Interface_Soket
from cryptography import fernet as f
import sessionManager as SM

host = "127.0.0.1"
port = 2000

#############################################################################
#
#                           Class
#
#############################################################################

class UI_Channel_Manager:
    def __init__(self, channelName, key):
        self.channelLog = []
        self.channelName = name
        self.key = f.Fernet.generate_key(key)
        self.key = Fernet(self.key)

    def sendMessage():
        SM.forwardMessage()
        return
    
    def updateLog():
        try:
            pickledLog = Interface_Soket.interface(host, port).send(pickle.dumps(['chatlog', self.channelName]))
            self.channelLog = pickle.loads(pickledLog)
            return self.channelLog
        except:
            return False


#[[tid,navn, besked],[tid,navn,besked],[tid,navn,besked]]



if __name__ == "__main__":
    print("Channel manager being run as main:")
    print("__________________________________")
    


