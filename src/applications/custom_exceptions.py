"""
Custom exceptions for the applications
"""


class ZeroArgumentsError(Exception):
    """
    Exception raised when no arguments are provided
    """
    def __init__(self, message):
        super().__init__(message)


class ExtraArgumentsError(Exception):
    """
    Exception raised when too many arguments are provided
    """
    def __init__(self, message):
        super().__init__(message)


class InsufficientArgumentsError(Exception):
    """
    Exception raised when too few arguments are provided
    """
    def __init__(self, message):
        super().__init__(message)


class InvalidArgumentsError(Exception):
    """
    Exception raised when too few arguments are provided
    """
    def __init__(self, message):
        super().__init__(message)


class IncorrectFlagError(Exception):
    """
    Exception raised when an incorrect flag is provided
    """
    def __init__(self, message):
        super().__init__(message)


class InvalidLinesRequestError(Exception):
    """
    Exception raised when line number a non-positive integer
    """
    def __init__(self, message):
        super().__init__(message)


class DirectoryNotFoundError(Exception):
    """
    Exception raised when a directory is not found
    """
    def __init__(self, message):
        super().__init__(message)


class InvalidRangeError(Exception):
    """
    Exception raised when a range is invalid
    """
    def __init__(self, message):
        super().__init__(message)
