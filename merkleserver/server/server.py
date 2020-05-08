#!/usr/bin/env python3

from merkletree import MerkleTree
import os
import socket

class Server:
    """Server Implementation. Designed to be installed onto Linux"""

    @classmethod
    def setup(cls):
        Server.debug = True
        Server.tree = MerkleTree()
        Server.file_dir = os.path.join(os.path.expanduser("~"), "MerkleFileStorage")
        if not os.path.exists(Server.file_dir): os.mkdir(Server.file_dir)
        Server.socket = socket.socket()
        Server.port = 55555
        if(Server.debug): print("Setup Complete") 

    @classmethod
    def start_server(cls):
        Server.setup()
        Server.run()
        Server.stop()

    @classmethod
    def run(cls):
        Server.socket.bind(("", Server.port))
        if(Server.debug): print("Binded to: {0}".format(Server.socket.getsockname())) 
        Server.socket.listen()
        if(Server.debug): print("Listening for Connections...") 
        conn, addr = Server.socket.accept()
        with conn:
            print("Accepted Connection from {0}".format(addr))
            while True:
                init_msg = conn.recv(1024)
                if not init_msg:
                    break
                else:
                    print("Message from client: {0}".format(init_msg))
                    print("Sending Message: Hello!")
                    conn.sendall(b"Hello!")

    @classmethod
    def stop(cls):
        Server.socket.close()

    @classmethod
    def print_tree(cls):
        if(Server.tree is not None):
            print(Server.tree)

def __main__():
    Server.start_server()
    Server.print_tree()

if __name__ == "__main__":
    __main__()