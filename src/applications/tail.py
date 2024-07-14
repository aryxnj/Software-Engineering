from collections import deque
import os
from .custom_exceptions import InsufficientArgumentsError
from .custom_exceptions import IncorrectFlagError
from .custom_exceptions import InvalidLinesRequestError


'''
The `Tail` class implements functionality similar to the Unix 'tail' command.
It is used to read the last n lines of a file.

Attributes:
    out: A deque used for storing the lines read from the file.

Methods:
    #tail:
    - Processes input arguments to determine the file and the number of lines
      to be read from the end of the file.
    - Includes extensive error handling for incorrect command line arguments
      and invalid flags.
    - Calls `tail_execute` to perform the actual reading of the file.

    #tail_check_valid_file:
    - Validates the existence and readability of the file path provided in
      the arguments.
    - Raises ValueError if the file does not exist or is not accessible.

    #tail_execute:
    - Reads the specified number of lines from the end of the file.
    - Handles the output either by appending to 'out' or returning a list of
      lines, based on the 'check_bit'.
'''


class Tail:
    def __init__(self):
        self.out = deque()

    def tail(self, args, out, check_bit):
        num_lines = 10
        if len(args) != 1 and len(args) != 2 and len(args) != 3:
            raise InsufficientArgumentsError("tail: wrong number of arguments")
        elif len(args) == 1:
            # file = args[0].getText()
            if type(args[0]) == str:
                file = args[0]
            else:
                file = args[0].getText()
            self.tail_check_valid_file(file)
            self.tail_execute(file, num_lines, check_bit)
        elif len(args) == 2:
            # file = args[1].getText()
            if type(args[1]) == str:
                file = args[1]
            else:
                file = args[1].getText()
            self.tail_check_valid_file(file)
            self.tail_execute(file, num_lines, check_bit)
        elif len(args) == 3:
            if args[0].getText() != "-n":
                raise IncorrectFlagError("tail: wrong flag, use -n")
            elif not args[1].getText().isdigit():
                raise InvalidLinesRequestError("tail: for line no. "
                                               "use a positive integer")
            else:
                # file = args[2].getText()
                if type(args[2]) == str:
                    file = args[2]
                else:
                    file = args[2].getText()
                num_lines = int(args[1].getText())
                self.tail_check_valid_file(file)
                self.tail_execute(file, num_lines, check_bit)

    def tail_check_valid_file(self, file):
        if not os.path.isfile(file):
            raise FileNotFoundError("tail: " + file +
                                    ": No such file or directory")
        return

    def tail_execute(self, file, num_lines, check_bit):
        string_list = []
        with open(file) as f:
            lines = f.readlines()
            display_length = min(len(lines), num_lines)
            for i in range(0, display_length):
                string_list.append(lines[len(lines) - display_length + i])
                if check_bit == 0:
                    self.out.append(lines[len(lines) - display_length + i])
        if check_bit == 1:
            return string_list
