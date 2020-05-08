#!/usr/bin/env python3

import socket

class Client:
    def __init__(self):
        self.setup()
        self.run()
        self.stop()

    def setup(self):
        self.debug = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if(self.debug): print("Setup complete.")
    
    def send_message(self, message):
        self.socket.sendall(message)
    
    def receive_message(self):
        return self.socket.recv(1024)

    def run(self):
        self.port = 55555
        # self.address = "192.168.0.100"
        self.address = "127.0.0.1"
        self.socket.connect((self.address, self.port))
        if(self.debug): print("Connecting to: {0}".format(self.socket.getsockname())) 
        self.send_message(b"Hello World!")
        data = self.receive_message()
        print('Received: {0}'.format(data))
    
    def stop(self):
        self.socket.close()

def __main__():
    client = Client()

if __name__ == "__main__":
    __main__()