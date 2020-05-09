from tree import Node
import hashlib
import secrets
import binascii

class MerkleTree:
    """Implementation of the Merkle Tree"""
    def __init__(self, files):
        self.root = None                # Root Node
        self.bitrate = 576              # Block size of hash in bits
        self.output_bitsize = 512       # Output size of hash in bits
        self.references = {}            # Dictionary of file references
        self.max_size = 2               # Max number before restructuring
        self.compute_tree(files)
    
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
    
    def get_hash(self, file_path):
        """Gets the SHA3_512 hash of the file"""
        bitrate = 576   # This is equivalent to the "blocksize" in SHA-2.
        with open(file_path, "rb") as unhashed_file:
            buf = unhashed_file.read(bitrate)
            hasher = hashlib.new("sha3_512")
            while len(buf) > 0:
                hasher.update(buf)
                buf = unhashed_file.read(bitrate)
        return hasher.digest()

    def combine_hashes(self, left, right):
        bitrate = 576
        hasher = hashlib.new("sha3_512")
        hasher.update(left)
        hasher.update(right)
        return hasher.digest()

    def generate_references(self, files):
        for file_path in files:
            digest = self.get_hash(file_path)
            self.references[file_path] = Node(digest)

    def compute_tree_recursive(self, reference_keys):
        length = len(reference_keys)
        if(length == 0): # This branch should never be reached, unless we start out with zero files
            return Node(None)
        elif(length == 2):
            left = self.references[reference_keys[0]]
            right = self.references[reference_keys[1]]
            digest = self.combine_hashes(left.value, right.value)
            new_node = Node(value=digest,left=left, right=right)
            return new_node
        elif(length == 1):
            left = self.references[reference_keys[0]]
            right = Node(secrets.token_bytes(self.output_bitsize//8))     # input takes bytes
            digest = self.combine_hashes(left.value, right.value)
            new_node = Node(value=digest, left=left, right=right)
            return new_node
        else:
            left = self.compute_tree_recursive(reference_keys[:length//2])
            right = self.compute_tree_recursive(reference_keys[length//2:])
            digest = self.combine_hashes(left.value, right.value)
            new_node = Node(value=digest, left=left, right=right)
            return new_node

    def compute_tree(self, files):
        self.generate_references(files)
        keys = list(self.references.keys())
        self.root = self.compute_tree_recursive(keys)

    @edit
    def add(self, file_path):
        """Adds a file to the tree"""
        hash = get_hash(file_path)
        print(hash)
        self.hash_list.append(hash)

        