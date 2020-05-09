#!/usr/bin/env python3

import socket
import os

class Client:
    def __init__(self):
        self.setup()
        self.run()
        self.stop()

    def setup(self):
        self.debug = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 55555
        # self.address = "192.168.0.100"
        self.address = "127.0.0.1"
        if(self.debug): print("Setup complete.")
    
    def send_message(self, message):
        print("[Client]: {0}".format(message))
        self.socket.sendall(str.encode(message))
    
    def receive_message(self):
        message = self.socket.recv(1024).decode("utf-8")
        print("[Server]: {0}".format(message))
    
    def upload_file(self, filepath):
        basename = os.path.basename(filepath)
        print("Uploading File: {}".format(basename))
        with open(filepath, 'rb') as file2send:
            size = self.socket.sendfile(file2send)
            print(size)
            # while data := file2send.read(1024):
            #     self.socket.sendall(data)
            # self.socket.sendall(b"Badly Implemented End of File Message")
        print("Uploaded File: {}".format(basename))

    def get_filepath(self):
        done = False
        path = None
        while not done:
            path = input("Input an empty message to exit.\n[Enter File Path]: ").strip()
            if os.path.exists(path):
                basename = os.path.basename(path)
                size = os.path.getsize(path)
                print("Sending File '{0}' of size {1}".format(basename, size))
                self.send_message("{0}:{1}".format(basename, size))
                done = True
            elif path == "":
                path = None
                self.send_message("No More Files")
                done = True
            else:
                print("Path does not exist!")
        return path

    def send_files(self):
        done = False
        while not done:
            path = self.get_filepath()
            if path is not None:
                self.upload_file(path)
            else:
                done = True

    def run(self):
        self.socket.connect((self.address, self.port))
        if self.debug: print("Connecting to: {0}".format(self.socket.getsockname()))
        self.receive_message()
        self.cli()

    def cli(self):
        done = False
        while not done:
            command = input("Input Command> ").strip()
            list_of_commands = ["sendfiles", "exit"]
            if command in list_of_commands:
                self.send_message(command)
                if command == "sendfiles":
                    self.send_files()
                elif command == "exit":
                    done = True
            else:
                print("Given command does not exist.")
    
    def stop(self):
        self.socket.close()

def __main__():
    client = Client()

if __name__ == "__main__":
    __main__()