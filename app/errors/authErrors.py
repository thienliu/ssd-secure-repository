class InvalidLoginSessionError(Exception):
    def __init__(self):
        super().__init__()

class InvalidCurrentPasswordError(Exception):
    def __init__(self):
        super().__init__()

class PasswordMismatchError(Exception):
    def __init__(self):
        super().__init__()

class UserNotExistError(Exception):
    def __init__(self, email):
        self.user_email = email
        super().__init__()
class UserDeletionError(Exception):
    def __init__(self, user_id):
        super().__init__()