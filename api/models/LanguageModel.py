from api.exceptions.LanguageNotSupported import LanguageNotSupported


class Language:
    def __init__(self, name, version):
        self.name = name
        self.version = version

    def getExtensionFile(self):
        match self.name:
            case "java":
                return "java"
            case "javascript":
                return "js"
            case _:
                raise LanguageNotSupported()