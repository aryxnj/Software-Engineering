from collections import deque
import re
import os
from .custom_exceptions import ZeroArgumentsError, InsufficientArgumentsError

'''
The `Grep` class implements a basic version of the grep command.
It searches for patterns within files and displays matching lines.

Attributes:
    out (collections.deque): A deque used for storing the results
    of grep operations.

Methods:
    #grep:
    - Processes input arguments and executes the grep search operation.
    - Includes error handling for cases like missing arguments, patterns,
      or file names.
    - Calls `grep_execute` to perform the actual search operation.

    #check_valid_files:
    - Validates file paths provided in the arguments.
    - Checks for the existence of files and read permissions.
    - Raises ValueError if any file is not found or is not accessible.

    #grep_execute:
    - Executes the core grep functionality.
    - Searches for the given pattern in the specified files.
    - Handles the output formatting based on whether single or multiple
      files are involved.
'''


class Grep:
    def __init__(self):
        self.out = deque()

    def grep(self, args, out, checkbit):
        if len(args) == 0:
            raise ZeroArgumentsError("grep: missing args, "
                                     "add pattern + file names")
        elif len(args) == 1:
            raise InsufficientArgumentsError("grep: missing args, "
                                             "add file names")
        elif len(args) >= 2:
            # Once we have ensured that there are at least 2 arguments,
            # we can check for valid files
            self.check_valid_files(args)
            # If all files are valid, we can execute the grep command
            self.grep_execute(args)

    def check_valid_files(self, args):
        files = args[1:]
        for file in files:
            if not os.path.isfile(file.getText()):
                raise FileNotFoundError("grep: " + file.getText() +
                                        ": No such file")
        return

    def grep_execute(self, args):
        pattern = args[0].getText().replace("'", "")
        files = args[1:]
        for file in files:
            with open(file.getText()) as f:
                lines = f.readlines()
                for line in lines:
                    if re.match(pattern, line):
                        if len(files) > 1:
                            file_temp = file.getText()
                            self.out.append(f"{file_temp}:{line}")
                        else:
                            self.out.append(line)
