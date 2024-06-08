class KeyNotFound(Exception):
    def __init__(self, message="Key not found. Id does not exist."):
        self.message = message
        super().__init__(self.message)
