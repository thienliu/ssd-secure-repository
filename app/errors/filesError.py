class FileAlreadyExistsError(Exception):
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__()

class FileInsertionError(Exception):
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__()