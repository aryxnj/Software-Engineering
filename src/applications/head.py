from collections import deque
import os
from .custom_exceptions import (
    InsufficientArgumentsError,
    IncorrectFlagError,
    InvalidLinesRequestError)

'''
The `Head` class implements functionality similar to the Unix 'head' command.
It is used to read the first n lines of a file.

Attributes:
    out: A deque used for storing the lines read from the file.

Methods:
    #head:
    - Processes input arguments to determine the file and the number of lines
      to be read.
    - Includes extensive error handling for incorrect command line arguments
      and invalid flags.
    - Calls `head_execute` to perform the actual reading of the file.

    #head_check_valid_file:
    - Validates the existence and readability of the file path provided in
      the arguments.
    - Raises ValueError if the file does not exist or is not accessible.

    #head_execute:
    - Reads the specified number of lines from the beginning of the file.
    - Handles the output either by appending to 'out' or returning a list
      of lines, based on the 'check_bit'.
    - If 'check_bit' is 0, the lines are appended to 'out'. If it's 1, the
      lines are returned as a list.
'''


class Head:
    def __init__(self):
        self.out = deque()

    def head(self,  args, out, check_bit):
        num_lines = 10
        if len(args) != 1 and len(args) != 2 and len(args) != 3:
            raise InsufficientArgumentsError("head: wrong number of arguments")
        elif len(args) == 1:
            if type(args[0]) == str:
                file = args[0]
            else:
                file = args[0].getText()
            self.head_check_valid_file(file)
            self.head_execute(file, num_lines, check_bit)
        elif len(args) == 2:
            # file = args[1].getText()
            if type(args[1]) == str:
                file = args[1]
            else:
                file = args[1].getText()
            self.head_check_valid_file(file)
            self.head_execute(file, num_lines, check_bit)
        elif len(args) == 3:
            if args[0].getText() != "-n":
                raise IncorrectFlagError("head: wrong flag, use -n")
            elif not args[1].getText().isdigit():
                raise InvalidLinesRequestError("head: for line no., "
                                               "use a positive integer")
            else:
                if type(args[2]) == str:
                    file = args[2]
                else:
                    file = args[2].getText()
                num_lines = int(args[1].getText())
                self.head_check_valid_file(file)
                self.head_execute(file, num_lines, check_bit)

    def head_check_valid_file(self, file):
        if not os.path.isfile(file):
            raise FileNotFoundError("head: " + file +
                                    ": No such file or directory")
        return

    def head_execute(self, file, num_lines, check_bit):
        string_list = []
        with open(file) as f:
            lines = f.readlines()
            for i in range(0, min(len(lines), num_lines)):
                string_list.append(lines[i])
                if check_bit == 0:
                    self.out.append(lines[i])
        if check_bit == 1:
            return string_list
