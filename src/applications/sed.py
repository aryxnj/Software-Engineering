import re
import os
from collections import deque
import codecs
from .custom_exceptions import (
    IncorrectFlagError,
    InsufficientArgumentsError,
    InvalidArgumentsError,
)

'''
The Sed class provides functionality similar to the Unix 'sed' command,
specifically for stream editing of text within files.

Attributes:
    out: A deque used for storing the results of the sed operation.

Methods:
    #sed:
    - Processes input arguments to determine the file and the pattern
      for substitution.
    - Includes error handling for incorrect argument number, file
      access issues, and pattern validation.
    - Calls exec to handle the substitution operation.

    #exec:
    - Main execution function that opens the specified file and calls
      process_substitution.
    - Raises InsufficientArgumentsError for incorrect argument count
      and FileNotFoundError for file access issues.

    #process_substitution:
    - Validates and processes the substitution pattern.
    - Splits the pattern to extract components for the replacement
      operation.
    - Calls replace with extracted pattern components.
    - Raises InvalidArgumentsError for incorrect pattern structure.

    #replace:
    - Performs the actual substitution in the file content.
    - Handles global ('g') and single occurrence replacement
      based on the provided flag.
    - Raises IncorrectFlagError for incorrect or unknown flags
      in the substitution pattern.

Exceptions:
    InsufficientArgumentsError: Raised if the number of arguments
    is incorrect.
    InvalidArgumentsError: Raised if the substitution pattern
    is invalid.
    IncorrectFlagError: Raised if an incorrect flag is used
    in the substitution pattern.
    FileNotFoundError: Raised if the specified file cannot
    be found or accessed.
'''


class Sed:
    def __init__(self):
        self.out = deque()

    def sed(self, args, out, checkBit):
        # print("in sed")
        args1 = []
        output = []
        for x in args:
            # if isinstance(x, TerminalNodeImpl):
            #     continue
            # else:
            args1.append(x.getText())

        # print("args1: ", args1)
        def exec(args):
            if len(args) == 2:
                cwd = os.getcwd()
                file_name = args[1]
                file_path = os.path.join(cwd, file_name)
                try:
                    with codecs.open(
                        file_path, "r", encoding="utf-8"
                    ) as file:
                        process_substitution(file, args[0])
                except IOError:
                    raise FileNotFoundError("can't find " + file_name)
            else:
                raise InsufficientArgumentsError("wrong number of arguments")

        def process_substitution(file, pattern):
            if pattern[0] != "'" or pattern[-1] != "'":
                raise InvalidArgumentsError("wrong pattern")
            pattern = pattern[1:-1]
            sub_pattern = pattern.split(pattern[1])
            # print(sub_pattern)
            if len(sub_pattern) != 4 or sub_pattern[0] != "s":
                raise InvalidArgumentsError("wrong pattern")
            replace(file, sub_pattern[1], sub_pattern[2], sub_pattern[3])

        def replace(file, old, new, flag):
            if flag == "g":
                for line in file:
                    # self.out.append(re.sub(old, new, line))
                    output.append(re.sub(old, new, line))
            elif flag == "":
                for line in file:
                    # self.out.append(re.sub(old, new, line, count=1))
                    output.append(re.sub(old, new, line, count=1))
            else:
                raise IncorrectFlagError("wrong flag")

        exec(args1)
        # print("outpittttt: ", output)
        return output
        # print("out: ", out)
        # for line in output:
        #     self.out.append(line + "\n")
