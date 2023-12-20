class DatabaseException(Exception):
    pass


class NoData(DatabaseException):
    pass


class NoUser(DatabaseException):
    pass


class NoRecipient(NoUser):
    pass


class UsernameTaken(DatabaseException):
    pass


class NoMessages(DatabaseException):
    pass
