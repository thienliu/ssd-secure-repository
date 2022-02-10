class FileAlreadyExistsError(Exception):
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__()

class FileInsertionError(Exception):
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__()

class FileUpdateError(Exception):
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__()
class FileDeletionError(Exception):
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__()

class FileNotExistsError(Exception):
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__()