class ImagePulledNotFound(Exception):
    def __init__(self, message="Image not found. Maybe language or version not supported."):
        self.message = message
        super().__init__(self.message)
