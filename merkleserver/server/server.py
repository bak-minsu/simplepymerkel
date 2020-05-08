from merkletree import MerkleTree 

class Server:
    """Server Implementation. Designed to be installed onto Linux"""
    @classmethod
    def start_server(cls):
        Server.tree = MerkleTree()
    
    @classmethod
    def print_tree(cls):
        if(Server.tree is not None):
            print(Server.tree)

def __main__():
    Server.start_server()
    Server.print_tree()

if __name__ == "__main__":
    __main__()