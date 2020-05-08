class Node:
    """Simple Binary Tree Node"""
    def __init__(self, value, left=None, right=None, parent=None):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

    def print2D(self, prefix, isLeft, final):
        if(self.right is not None):
            print("Right not empty")
            new_prefix = prefix + ("│        " if isLeft else "         ")
            self.right.print2D(new_prefix, False, final)
        final.append(prefix + ("└─────── " if isLeft else "┌─────── ") + str(self.value) + "\n")
        if(self.left is not None):
            print("Left not empty")
            new_prefix = prefix + ("         " if isLeft else "│        ")
            self.left.print2D(new_prefix, True, final)
        return "".join(final)

    def __str__(self):
        return self.print2D("", True, [])