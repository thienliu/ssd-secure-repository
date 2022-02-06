class InvalidLoginSessionError(Exception):
    def __init__(self):
        super().__init__()

class InvalidCurrentPasswordError(Exception):
    def __init__(self):
        super().__init__()

class PasswordMismatchError(Exception):
    def __init__(self):
        super().__init__()