import socket

class interface:
    def __init__(self, hostip, port):
        self.port = port
        self.host = hostip

    def send(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(message)
            data = s.recv(1024)
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            return data

    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            conn, addr = s.accept()
            while True:
                data = conn.recv(1024)
                if not data:
                    break

    # def ipv6test(self):
    #     with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
    #         s.connect(("fe80::2b86:9f3d:6114:ac1c", 9999))
    #         s.sendall(b"Din mor")
    #         data = s.recv(1024)
    #         s.close()



if __name__ == "__main__":
    test = send(9999)
    test.ipv6test()
