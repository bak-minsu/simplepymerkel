#!/usr/bin/env python3

from merkletree import MerkleTree
import os
import socket

class Server:
    """Server Implementation. Designed to be installed onto Linux"""

    @classmethod
    def setup(cls):
        cls.debug = True
        cls.tree = None
        cls.file_dir = None
        cls.tree_iteration = 0
        cls.socket = socket.socket()
        cls.port = 55555
        cls.instantiate_server_dir()
        if cls.debug: print("Setup Complete") 

    @classmethod
    def instantiate_server_dir(cls):
        cls.file_dir = os.path.join(os.path.expanduser("~"), "MerkleFileStorage")
        if not os.path.exists(cls.file_dir): os.mkdir(cls.file_dir)
        cls.generate_tree()
        cls.save_tree()

    @classmethod
    def generate_tree(cls):
        files = []
        for stored_file in os.listdir(cls.file_dir):
            full_path = os.path.join(cls.file_dir, stored_file)
            files.append(full_path)
        cls.tree = MerkleTree(files)

    @classmethod
    def stop(cls):
        cls.socket.close()

    @classmethod
    def start_server(cls):
        cls.setup()
        cls.run()
        cls.stop()

    @classmethod
    def run(cls):
        connection = cls.wait_for_connection()
        cls.handle_connection(connection)

    @classmethod
    def wait_for_connection(cls):
        cls.socket.bind(("", cls.port))
        if cls.debug: print("Binded to: {0}".format(cls.socket.getsockname())) 
        cls.socket.listen()
        if cls.debug: print("Listening for Connections...")
        return cls.socket.accept()

    @classmethod
    def send_message(cls, message, conn_object):
        print("[Server]: {0}".format(message))
        conn_object.sendall(str.encode(message))
    
    @classmethod
    def receive_message(cls, conn_object):
        message = conn_object.recv(1024).decode("utf-8")
        print("[Client]: {0}".format(message))
        return message

    @classmethod
    def download_file(cls, filename, size, conn_object):
        path = os.path.join(cls.file_dir, filename)
        print("Downloading File '{0}' of size {1}".format(filename, size))
        with open(path, 'wb') as received_file:
            total_bytes = 0
            while total_bytes < size:
                data = conn_object.recv(size)
                total_bytes += len(data)
                received_file.write(data)
        print("Downloaded File '{0}' of size {1}".format(filename, size))
        
    @classmethod
    def receive_files(cls, conn_object):
        print("Set to receive files.")
        receive_more = True
        while receive_more:
            message = cls.receive_message(conn_object)
            if message != "No More Files":
                filename, size = message.split(":")
                print("Receiving File '{0}' of size {1}".format(filename, size))
                cls.download_file(filename, int(size), conn_object)
                cls.tree.add(os.path.join(cls.file_dir, filename))
                cls.save_tree()
            else: receive_more = False
        print("Completed receiving Files.")

    @classmethod
    def handle_connection(cls, connection):
        conn_object, addr = connection
        with conn_object:
            print("Accepted Connection from {0}".format(addr))
            cls.send_message("Hello Client! Send a Command!", conn_object)
            cls.cli(conn_object)
    
    @classmethod
    def cli(cls, conn_object):
        done = False
        while not done:
            command = cls.receive_message(conn_object)
            print("Recieved Command: {0}".format(command))
            if command == "sendfiles":
                cls.receive_files(conn_object)
            elif command == "exit":
                done = True

    @classmethod
    def save_tree(cls):
        if cls.tree is not None:
            filename = "tree_{0}.txt".format(cls.tree_iteration) 
            with open(filename, "w", encoding="utf-8") as tree_file:
                tree_file.write(str(cls.tree))
            cls.tree_iteration += 1

def __main__():
    Server.start_server()

if __name__ == "__main__":
    __main__()