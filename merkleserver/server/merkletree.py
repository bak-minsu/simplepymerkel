from tree import Node
import hashlib
import math
import binascii
import os

class MerkleTree:
    """Implementation of the Merkle Tree"""
    def __init__(self, files):
        self.root = None                # Root Node
        self.bitrate = 576              # Block size of hash in bits
        self.output_bitsize = 512       # Output size of hash in bits
        self.references = {}            # Dictionary of file references
        self.max_size = 2               # Max number before restructuring
        self.tree_iteration = 0
        self.init_tree(files)
    
    def __str__(self):
        if self.root is not None:
            return self.root.__str__()
        else: return "No Files in Directory"
    
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
        references = {}
        for file_path in files:
            digest = self.get_hash(file_path)
            references[file_path] = Node(digest)
        return references

    def compute_tree_recursive(self, nodes):
        length = len(nodes)
        if length == 2:
            left = nodes[0]
            right = nodes[1]
            digest = self.combine_hashes(left.value, right.value)
            new_node = Node(value=digest,left=left, right=right)
            return new_node
        else:
            left = self.compute_tree_recursive(nodes[:length//2])
            right = self.compute_tree_recursive(nodes[length//2:])
            digest = self.combine_hashes(left.value, right.value)
            new_node = Node(value=digest, left=left, right=right)
            return new_node
    
    def get_default_hash(self):
        hasher = hashlib.new("sha3_512")
        hasher.update(b"Default Value")
        return hasher.digest()

    def compute_tree(self):
        self.references = self.generate_references(files)
        nodes = list(self.references.values())
        ref_len = len(nodes)
        if ref_len == 0:
            return None
        elif ref_len == 1:
            nodes.append(Node(self.get_default_hash()))
        elif not math.log2(ref_len).is_integer() :
            # Add default leaves
            closest_power_of_2 = math.ceil(math.log2(ref_len))
            diff = int(math.pow(2, closest_power_of_2)) - ref_len
            for _ in range(diff):
                new_node = Node(self.get_default_hash())
                nodes.append(new_node)
        tree = self.compute_tree_recursive(nodes)
        return tree

    def init_tree(self, files):
        if len(files) > 0:
            self.root = self.compute_tree()
            self.save_tree()
        else:
            return None

    def refresh_proofs(self):
        self.root = self.compute_tree()

    def add(self, file_path):
        """Adds a file to the tree"""
        digest = self.get_hash(file_path)
        self.references[file_path] = Node(digest)
        keys = list(self.references.keys())
        self.refresh_proofs()
        self.save_tree()

    def get_proof(self, file_path):
        """Returns proof for given file_path"""
        self.refresh_proofs()
        prooflist = []
        current_node = self.references[file_path]
        while current_node.parent is not None:
            if current_node.parent.left is current_node:
                prooflist.append("R:" + current_node.parent.right.get_value_in_str())
            elif current_node.parent.right is current_node:
                prooflist.append("L:" + current_node.parent.left.get_value_in_str())
            current_node = current_node.parent
        return prooflist

    def save_tree(self):
        if self.root is not None:
            if not os.path.exists("./trees"): os.mkdir("./trees")
            filename = "./trees/tree_{0}.txt".format(self.tree_iteration) 
            with open(filename, "w", encoding="utf-8") as tree_file:
                tree_file.write(str(self))
            self.tree_iteration += 1