from tree import Node
from hashlib import sha3_512 as hash
from secrets import randbits

class MerkleTree:
    """Implementation of the Merkle Tree"""
    def __init__(self):
        self.root = Node(0)             # Root Node
        self.references = {}            # List of file references
        self.max_size = 2               # Max number before restructuring
    
    def __str__(self):
        return self.root.__str__()

    def recompute():
        print("Recomputing!")

    def edit(self):
        """
        This decorator marks that the function edits the tree.
        It recomputes the tree if necessary.
        """
        def call_function(*args, **kwargs):
            if len(reference_list) > self.max_size:
                recompute()
        return call_function
    
    def get_hash(file_path):
        """Gets the SHA3_512 hash of the file"""
        bitrate = 576   # This is equivalent to the "blocksize" in SHA-2.
        with open(file_path, "rb") as unhashed_file:
            buf = unhashed_file.read(bitrate)
            while len(buf) > 0:
                hash.update(buf)
                buf = unhashed_file.read(bitrate)

    @edit
    def add(self, file_path):
        """Adds a file to the tree"""
        hash = get_hash(file_path)
        print(hash)
        self.hash_list.append(hash)

        