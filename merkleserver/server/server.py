import os

class Server:
    """Server Implementation. Designed to be installed onto Linux"""

    @classmethod
    def create_test_file_dir(cls):
        Server.test_file_dir = os.path.join(os.path.expanduser('~'), "MerkleServerTestFiles")

    @classmethod
    def start_server(cls):
        Server.tree = MerkleTree()
    
    @classmethod
    def print_tree(cls):
        if(Server.tree is not None):
            print(Server.tree)

    @classmethod
    def create_test_files(cls):
        Server.create_test_file_dir()
        mkdir(Server.test_file_dir)
        if platform.system() == "Linux":
            system("truncate -s 5M answers_to_test.txt")
        elif platform.system() == "Windows":
            system("fsutil file createnew answers_to_test.txt")
        else:
            print("This command isn't supported for your OS. Supported OS: Windows, Linux")


def __main__():
    Server.start_server()
    Server.print_tree()

if __name__ == "__main__":
    __main__()