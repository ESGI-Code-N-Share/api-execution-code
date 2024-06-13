class LanguageNotSupported(Exception):
    def __init__(self, message="Language is not supported"):
        self.message = message
        super().__init__(self.message)
