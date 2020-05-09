import binascii

class Node:
    """Simple Binary Tree Node"""
    def __init__(self, value, left=None, right=None, parent=None):
        self.value = value
        self.left = None
        self.right = None
        self.add_children(left, right)
        self.parent = parent

    def hex_to_str(self, hex):
        return binascii.hexlify(hex).decode("utf-8")

    def tree_str(self, prefix, isLeft, final):
        if(self.right is not None):
            new_prefix = prefix + ("│        " if isLeft else "         ")
            self.right.tree_str(new_prefix, False, final)
        value_str = self.hex_to_str(self.value)[:8] # Gets the first 8 characters
        final.append(prefix + ("└─────── " if isLeft else "┌─────── ") + value_str + "\n")
        if(self.left is not None):
            new_prefix = prefix + ("         " if isLeft else "│        ")
            self.left.tree_str(new_prefix, True, final)
        return "".join(final)

    def __str__(self):
        return self.tree_str("", True, [])

    def add_children(self, left=None, right=None):
        if left is not None:
            self.left = left
            left.parent = self
        if right is not None:
            self.right = right
            right.parent = self