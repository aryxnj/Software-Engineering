from collections import deque
import os
from .custom_exceptions import (
    ZeroArgumentsError,
    DirectoryNotFoundError,
    ExtraArgumentsError)

'''
The `Cd` class provides functionality to change the current working directory.

Attributes:
    out: A deque used for storing output messages or command results.

Methods:
    #cd:
    -Changes the current working directory based on provided arguments.
    -It handles special cases like navigating to the parent directory
     and checks for valid directory paths.
    -Error handling includes checking for non-existent directories,
     permission issues, and incorrect argument counts.
'''


class Cd:
    def __init__(self):
        self.out = deque()

    def cd(self, args, out1, check_bit):
        if len(args) == 0:
            raise ZeroArgumentsError("cd: missing arguments, "
                                     "add directory name")
        elif args[0].getText() == "..":
            os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
            return
        elif not os.path.isdir(args[0].getText()):
            raise DirectoryNotFoundError("cd: " + args[0].getText() +
                                         ": No such file or directory")
        elif len(args) > 1:
            raise ExtraArgumentsError("cd: too many arguments, "
                                      "you can only cd into one "
                                      "directory at a time")
        else:
            os.chdir(args[0].getText())
