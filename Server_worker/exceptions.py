class DatabaseException(Exception):
    def __init__(self, message="A database error occurred."):
        self.message = message
        super().__init__(self.message)


class NoData(DatabaseException):
    def __init__(self, message="No data found."):
        super().__init__(message)


class NoUser(DatabaseException):
    def __init__(self, message="User not found."):
        super().__init__(message)


class NoRecipient(NoUser):
    def __init__(self, message="Recipient not found."):
        super().__init__(message)


class UsernameTaken(DatabaseException):
    def __init__(self, message="Username is already taken."):
        super().__init__(message)


class NoMessages(DatabaseException):
    def __init__(self, message="No messages found."):
        super().__init__(message)


class UserNotFoundError(NoUser):
    def __init__(self, username):
        message = f"No user with username {username} found."
        super().__init__(message)


class MessageInsertionError(DatabaseException):
    def __init__(self):
        message = "An error occurred while inserting the message."
        super().__init__(message)


class UserUpdateError(DatabaseException):
    def __init__(self):
        message = "An error occurred while updating the user."
        super().__init__(message)


class HashMismatchError(Exception):
    def __init__(self):
        self.message = "The provided hash does not match the hash of the message."
        super().__init__(self.message)
