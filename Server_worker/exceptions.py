"""
This module has custom exceptions that used in application.
"""


class DatabaseException(Exception):
    """
    Custom exception. Should be raised when error in database requests appear.
    """

    def __init__(self, message="A database error occurred."):
        self.message = message
        super().__init__(self.message)


class NoData(DatabaseException):
    """
    Custom exception. Should be raised when SQL query returns NULL.
    """

    def __init__(self, message="No data found."):
        super().__init__(message)


class NoUser(DatabaseException):
    """
    Custom exception. Should be raised when no user found with given username.
    """

    def __init__(self, message="User not found."):
        super().__init__(message)


class NoRecipient(NoUser):
    """
    Custom exception. Should be raised when no user found with given username, but when user is recipient.
    """

    def __init__(self, message="Recipient not found."):
        super().__init__(message)


class UsernameTaken(DatabaseException):
    """
    Custom exception. Should be raised when user with given username is already exists in users table, when try to write new user.
    """

    def __init__(self, message="Username is already taken."):
        super().__init__(message)


class NoMessages(DatabaseException):
    """
    Custom exception. Should be raised when no messages found with given criteria.
    """

    def __init__(self, message="No messages found."):
        super().__init__(message)


class UserNotFoundError(NoUser):
    """
    Custom exception. Should be raised when no user found with given username, but when user is sender.
    """

    def __init__(self, username):
        message = f"No user with username {username} found."
        super().__init__(message)


class MessageInsertionError(DatabaseException):
    """
    Custom exception. Should be raised when error occurs while inserting new message in messages table.
    """

    def __init__(self):
        message = "An error occurred while inserting the message."
        super().__init__(message)


class UserUpdateError(DatabaseException):
    """
    Custom exception. Should be raised when error occurs after try to update user's data.
    """

    def __init__(self):
        message = "An error occurred while updating the user."
        super().__init__(message)


class HashMismatchError(Exception):
    """
    Custom exception. Should be raised when user's message hash doesn't match with hash of last received message by user.
    """

    def __init__(self):
        self.message = "The provided hash does not match the hash of the message."
        super().__init__(self.message)
