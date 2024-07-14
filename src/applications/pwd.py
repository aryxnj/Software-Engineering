from collections import deque
import os
from .custom_exceptions import ExtraArgumentsError

'''
The `Pwd` class to displays the current working directory.

Attributes:
    out: A deque used for storing the output of the pwd operation.

Methods:
    #pwd:
    - Executes the pwd command without requiring any arguments.
    - Validates that no arguments are passed to the command.
    - Appends the current working directory to the 'out' deque.

Exceptions:
    ValueError: Raised if any arguments are passed to the pwd command.
'''


class Pwd:
    def __init__(self):
        self.out = deque()

    def pwd(self, args, out, check_bit):
        if len(args) > 0:
            raise ExtraArgumentsError("pwd: too many arguments")
        self.out.append(os.getcwd())
