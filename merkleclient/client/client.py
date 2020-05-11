#!/usr/bin/env python3

import socket
import os
import hashlib
import math
import binascii

class Client:
    def __init__(self):
        self.setup()
        self.run()
        self.stop()

    def setup(self):
        self.debug = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 55555
        self.file_dir = os.path.join(os.path.expanduser("~"), "ClientFiles")
        self.download_dir = os.path.join(os.path.expanduser("~"), "ClientDownload")
        self.digest = self.create_digest(self.get_all_files())
        print("Digest of all files: {0}".format(self.digest))
        # self.address = "192.168.0.100"
        # self.address = "127.0.0.1"
        self.address = "178.128.134.85"
        if(self.debug): print("Setup complete.")

    def send_message(self, message):
        print("[Client]: {0}".format(message))
        self.socket.sendall(message.encode("UTF-8"))
    
    def receive_message(self):
        message = self.socket.recv(1024).decode("utf-8")
        print("[Server]: {0}".format(message))
        return message
    
    def upload_file(self, filepath):
        basename = os.path.basename(filepath)
        size = os.path.getsize(filepath)
        print("Sending File '{0}' of size {1}".format(basename, size))
        self.send_message("{0}:{1}".format(basename, size))
        self.receive_message()
        print("Uploading File: {}".format(basename))
        with open(filepath, 'rb') as file2send:
            self.socket.sendfile(file2send, count=size)
        self.receive_message()
        print("Uploaded File: {}".format(basename))

    def get_filepath(self):
        done = False
        path = None
        while not done:
            path = input("Input an empty message to exit.\n[Enter File Path]: ").strip()
            if os.path.exists(path):
                done = True
                return path
            elif path == "":
                self.send_message("No More Files")
                done = True
                return None
            else:
                print("Path does not exist!")

    def send_files(self):
        done = False
        while not done:
            path = self.get_filepath()
            if path is not None:
                self.upload_file(path)
            else:
                done = True

    def receive_file(self, filename, size):
        self.send_message("Ready to Download File '{0}' of size {1}".format(filename, size))
        file_path = os.path.join(self.download_dir, filename)
        print("Downloading File '{0}' of size {1}".format(filename, size))
        with open(file_path, 'wb') as received_file:
            total_bytes = 0
            while total_bytes < size:
                data = self.socket.recv(size)
                total_bytes += len(data)
                received_file.write(data)
        print("Downloaded File '{0}' of size {1}".format(filename, size))
        print("Receiving Proof")
        prooflist = self.process_prooflist_str(self.receive_message())
        print("Received Proof")
        print("Verifying Proof")
        is_verified = self.proof_is_correct(file_path, prooflist)
        if is_verified: print("Proof Verified!")
        else: print("Proof Invalid. Files have been tampered.")
    
    def get_files(self):
        done = False
        while not done:
            filename = input("[File Name]: ").strip()
            if filename != "":
                self.send_message(filename)
                size = self.receive_message()
                if size != "File does not exist":
                    self.receive_file(filename, int(size))
            else:
                self.send_message("No More Files")
                done = True

    def get_hash(self, filepath):
        """Gets the SHA3_512 hash of the file"""
        if type(filepath) == str:
            bitrate = 576   # This is equivalent to the "blocksize" in SHA-2.
            with open(filepath, "rb") as unhashed_file:
                buf = unhashed_file.read(bitrate)
                hasher = hashlib.new("sha3_512")
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = unhashed_file.read(bitrate)
            return hasher.digest()
        elif type(filepath) == bytes:
            return filepath

    def combine_hashes(self, left, right):
        bitrate = 576
        hasher = hashlib.new("sha3_512")
        hasher.update(left)
        hasher.update(right)
        return hasher.digest()

    def create_digest_recursive(self, files):
        length = len(files)
        if length == 2:
            left = self.get_hash(files[0])
            right = self.get_hash(files[1])
            digest = self.combine_hashes(left, right)
            return digest
        else:
            left = self.create_digest_recursive(files[:length//2])
            right = self.create_digest_recursive(files[length//2:])
            digest = self.combine_hashes(left, right)
            return digest

    def get_default_hash(self):
        hasher = hashlib.new("sha3_512")
        hasher.update(b"Default Value")
        return hasher.digest()

    def create_digest(self, files):
        files_len = len(files)
        if files_len == 0:
            return None
        elif files_len == 1:
            files.append(self.get_default_hash())
        elif not math.log2(files_len).is_integer() :
            # Add default leaves
            closest_power_of_2 = math.ceil(math.log2(files_len))
            diff = int(math.pow(2, closest_power_of_2)) - files_len
            for _ in range(diff):
                files.append(self.get_default_hash())
        return self.create_digest_recursive(files)

    def get_all_files(self):
        files = []
        for stored_file in os.listdir(self.file_dir):
            full_path = os.path.join(self.file_dir, stored_file)
            files.append(full_path)
        return files

    def send_all_files(self):
        files = self.get_all_files()
        for stored_file in files:
            self.upload_file(stored_file)
        self.send_message("No More Files")

    def proof_is_correct(self, file_path, prooflist):
        cur_hash = self.get_hash(file_path)
        print("Initial Digest: {0}".format(self.short_hex(cur_hash)))
        for proof, direction in prooflist:
            new_hash = None
            if direction == "L":    # Proof is on the left
                new_hash = self.combine_hashes(proof, cur_hash)
            elif direction == "R":  # Proof is on the right
                new_hash = self.combine_hashes(cur_hash, proof)
            print("Combine {0} and {1} to create {2}".format(self.short_hex(cur_hash), self.short_hex(proof), self.short_hex(new_hash)))
            cur_hash = new_hash
        print("Final Proof Digest: {0}".format(self.short_hex(cur_hash)))
        return cur_hash == self.digest
        
    def str_to_hex(self, string):
        return binascii.unhexlify(string.encode())

    def hex_to_str(self, hex):
        return binascii.hexlify(hex).decode("utf-8")

    def short_hex(self, hex):
        return self.hex_to_str(hex)[:8]

    def process_prooflist_str(self, liststr):
        prooflist = []
        prooflist_decoded = liststr.strip("'][").split("', '")
        for proof_str in prooflist_decoded:
            direction, proof = proof_str.split(":")
            prooflist.append((self.str_to_hex(proof), direction))
        return prooflist

    def get_proof(self):
        done = False
        while not done:
            filename = input("[File Name]: ").strip()
            if filename != "":
                self.send_message(filename)
                prooflist_str = self.receive_message()
                if prooflist_str != "File does not exist":
                    prooflist = self.process_prooflist_str(prooflist_str)
                    filepath = os.path.join(self.file_dir, filename)
                    correctness = self.proof_is_correct(filepath, prooflist)
                    print("Proof is correct: {0}".format(correctness))
            else:
                self.send_message("Done with proofs")
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
            list_of_commands = ["sendfiles", "sendallfiles", "exit", "getproof", "getfiles"]
            if command in list_of_commands:
                self.send_message(command)
                if command == "sendfiles":
                    self.send_files()
                elif command == "sendallfiles":
                    self.send_all_files()
                elif command == "getproof":
                    self.get_proof()
                elif command == "getfiles":
                    self.get_files()
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