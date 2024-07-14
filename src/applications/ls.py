from collections import deque
import os
from os import listdir
from .custom_exceptions import DirectoryNotFoundError, ExtraArgumentsError

'''
The `Ls` class implements a basic version of the 'ls' command from
Unix-like systems for listing directory contents.

Attributes:
    out: A deque used for storing the output of the ls operation.

Methods:
    #ls:
    - Processes input arguments to determine the directory to be listed.
    - Handles cases with no arguments by using the current working
      directory.
    - Validates the argument count and checks if the provided path
      is a directory.
    - Calls `ls_execute` to perform the actual listing of the directory.

    #ls_execute:
    - Lists the contents of the specified directory.
    - Excludes hidden files (those starting with '.').
    - Depending on the value of 'check_bit', appends the output to 'out'
      or returns it as a list.
    - If 'check_bit' is 0, the output is appended to 'out'. If it's 1,
      the output is returned as a list.

Exceptions:
    ValueError: Raised if the number of arguments is incorrect.
    FileNotFoundError: Raised if the specified directory does not exist.
'''


class Ls:
    def __init__(self):
        self.out = deque()

    def ls(self, args, out, check_bit):
        if len(args) == 0:
            ls_dir = os.getcwd()
        elif len(args) > 1:
            raise ExtraArgumentsError("wrong number of command line arguments")
        else:
            ls_dir = args[0].getText()
            if not os.path.isdir(ls_dir):
                raise DirectoryNotFoundError("ls: " + ls_dir +
                                             "No such directory")
        self.ls_execute(ls_dir, check_bit)

    def ls_execute(self, ls_dir, check_bit):
        save_string = []
        for f in listdir(ls_dir):
            if not f.startswith("."):
                temp = f
                save_string.append(temp + "\n")
                if check_bit == 0:
                    self.out.append(temp + "\n")
        if check_bit == 1:
            return save_string
