#!/usr/bin/env python
import sys
import logging
import socket
import struct
import fcntl
import os
from util import *


logger = logging.getLogger()
clients = {}


def p2pServer(host='0.0.0.0', port=5005):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    s.settimeout(30)

    while True:
        try:
            conn, addr = s.accept()
        except socket.timeout:
            continue

        logger.info('connection address: %s', addr)
        data = recv_msg(conn)
        priv_addr = msg_to_addr(data)
        send_msg(conn, addr_to_msg(addr))
        data = recv_msg(conn)
        data_addr, token = msg_to_addr_tok(data)
        if data_addr == addr:
            logger.info('client reply matches. token: %s', token)
            clients[addr] = Client(conn, addr, priv_addr, token)
        else:
            logger.info('client reply did not match')
            conn.close()

        logger.info('server - received data: %s', data)
        match = 0
        for k in clients:
            if k == addr:
                continue
            if clients[k].token == token:
                logger.info('server - send client info to: %s', clients[addr].pub)
                send_msg(clients[addr].conn, clients[k].peer_msg())
                logger.info('server - send client info to: %s', clients[k].pub)
                send_msg(clients[k].conn, clients[addr].peer_msg())
                match = 1
                break
        if match == 1:
            clients.pop(k)
            clients.pop(addr)
            logger.info('items left in clients dictionary: %s', clients.items())
    conn.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(message)s')
    p2pServer()
