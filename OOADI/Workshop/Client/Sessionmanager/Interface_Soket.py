import socket
import pickle

class interface:
    def __init__(self, socket):
        self.port = 65432
        self.host = "nisker.win"
        self.BUFFER_SIZE = 8192
        self.socket = socket
        self.socket.connect((self.host, self.port))

    def send(self, message):
        try:
            self.socket.send(message)
        except:
            print("failed to send")
            return False



    def listen(self):
        res = self.socket.recv(self.BUFFER_SIZE)
        res = pickle.loads(res)
        return res

    # def ipv6test(self):
    #     with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
    #         s.connect(("fe80::2b86:9f3d:6114:ac1c", 9999))
    #         s.sendall(b"Din mor")
    #         data = s.recv(1024)
    #         s.close()



if __name__ == "__main__":
    i = interface()
    i.send(b"hallo")
    i.listen()

