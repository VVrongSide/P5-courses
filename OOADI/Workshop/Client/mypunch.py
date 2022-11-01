#!/usr/bin/env python
import sys
import logging
import socket
import struct
from threading import Event, Thread
from util import *

logger = logging.getLogger('client')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

class P2P:
    def __init__(self, Rhost = "nisker.win", Rport = 5005):
        self.STOP = Event()
        self.host = Rhost
        self.port = Rport

    def send(self, key):
        self.key = key
        self.manager()

    def get(self):
        self.key = ''
        self.manager()
        return self.key

    def manager(self):
        sa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sa.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        logger.info("Estabishing P2P trough %s:%s", self.host, self.port)
        sa.connect((self.host, self.port))
        priv_addr = sa.getsockname()

        send_msg(sa, addr_to_msg(priv_addr))
        data = recv_msg(sa)
        logger.debug("client %s %s - received data: %s", priv_addr[0], priv_addr[1], data)
        pub_addr = msg_to_addr(data)
        send_msg(sa, addr_to_msg_tok(pub_addr, "654"))

        data = recv_msg(sa)
        pubdata, privdata = data.split(b'|')
        client_pub_addr = msg_to_addr(pubdata)
        client_priv_addr = msg_to_addr(privdata)
        logger.debug(
            "client public is %s and private is %s, peer public is %s private is %s",
            pub_addr, priv_addr, client_pub_addr, client_priv_addr,
        )
        
        threads = {
            '1_connect': Thread(target=self.connect, args=(priv_addr, client_pub_addr,)),
            '0_accept': Thread(target=self.accept, args=(priv_addr[1],)),
            '1_accept': Thread(target=self.accept, args=(client_pub_addr[1],)),
            '2_connect': Thread(target=self.connect, args=(priv_addr, client_priv_addr,)),
        }

        for name in sorted(threads.keys()):
            threads[name].start()

        while threads:
            keys = list(threads.keys())
            for name in keys:
                try:
                    threads[name].join(1)
                except TimeoutError:
                    continue
                if not threads[name].is_alive():
                    threads.pop(name)

    def accept(self, port):
        logger.info("accept %s", port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.bind(('', port))
        s.listen(1)
        s.settimeout(5)
        while not self.STOP.is_set():
            try:
                conn, addr = s.accept()
            except socket.timeout:
                print("s.accept(): timeput")
                continue
            else:
                logger.info("Accept %s connected!", port)
        data = recv_msg(sa)
        print(data)
        self.STOP.set()

    def connect(self, local_addr, addr):
        logger.debug("connect from %s to %s", local_addr, addr)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.bind(local_addr)
        while not self.STOP.is_set():
            try:
                s.connect(addr)
            except socket.error:
                continue
            else:
                logger.debug("connected from %s to %s success!", local_addr, addr)
                if self.key == '':
                    self.key = s.recv(1024)
                    logger.debug(self.key)
                else:
                    s.send(self.key)
                self.STOP.set()
        s.close()

if __name__ == '__main__':
     p2p = P2P()
     #print(p2p.get())
     p2p.send(b'hej')
