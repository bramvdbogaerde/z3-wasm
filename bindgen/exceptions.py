
class CommandLineArgumentError(Exception): 
    """
    Can be raised when the user fails to provide a valid set of command line arguments
    """
    pass

class CouldNotParseHeader(Exception):
    """
    Can be raised when the header file cannot be parsed
    """

class UnexpectedASTNode(Exception):
    def __init__(self, node):
        self.node = node 

    def __str__(self):
        return f"Unrecognized node {self.node.kind}"
