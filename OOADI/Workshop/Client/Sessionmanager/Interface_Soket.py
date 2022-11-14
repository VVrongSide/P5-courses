import socket
import pickle

class interface:
    def __init__(self):
        self.port = 65432
        self.host = "nisker.win"
        self.BUFFER_SIZE = 1024

    def send(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.host, self.port))
                s.sendall(message)
                mes = s.recv(self.BUFFER_SIZE)
                mes = pickle.loads(mes)
                return mes
            except:
                print("failed to send")
                return False



    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            res = s.recv(self.BUFFER_SIZE)
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

