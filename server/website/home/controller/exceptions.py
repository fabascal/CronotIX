# website/home/controller/exceptions.py

class FunctionNotFoundError(Exception):
    """Exception raised when a function is not found in the Functions object."""
    def __init__(self, message="Function not found"):
        self.message = message
        super().__init__(self.message)
