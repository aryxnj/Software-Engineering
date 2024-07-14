from collections import deque
from .custom_exceptions import ExtraArgumentsError
from .custom_exceptions import IncorrectFlagError
from .custom_exceptions import ZeroArgumentsError

'''
The `Uniq` class implements functionality similar to the Unix 'uniq' command.
Filters out adjacent repeated lines in a file.

Attributes:
    out: A deque used for storing the unique lines read from the file.

Methods:
    #uniq:
    - Takes arguments to determine file and whether to consider case
      sensitivity.
    - Includes error handling for incorrect CL arguments and unknown flags.
    - Calls either `uniq_handle_two_args` or `uniq_handle_one_arg`
      based on the number of arguments.

    #uniq_handle_invalid_args:
    - Handles cases of wrong argument count or unrecognized flags.
    - Raises ValueError with specific error messages based on the argument
      issues.

    #uniq_handle_two_args:
    - Handles the case of two arguments where the first one is a
      flag ("-i" for case-insensitivity).
    - Reads from the specified file and filters out repeated lines,
      ignoring case if specified.
    - Appends unique lines to 'out'.

    #uniq_handle_one_arg:
    - Handles the case of a single argument which is the file name.
    - Reads from the file and filters out repeated lines considering
      case sensitivity.
    - Appends unique lines to 'out'.
'''


class Uniq:
    def __init__(self):
        self.out = deque()

    def uniq(self, args, out, check_bit):
        args1 = []
        for x in args:
            if type(x) != str:
                args1.append(x.getText())
            else:
                args1.append(x)
        if len(args1) == 0 or (len(args1) != 1 and
                               args1[0] != "<" and
                               args1[0] != "-i"):
            self.uniq_handle_invalid_args(args1)
        else:
            if len(args1) == 2 and args1[0] == "-i":
                file = args1[1]
                self.uniq_handle_two_args(file, True)
            else:
                file = args1[0]
                self.uniq_handle_one_arg(file)

    def uniq_handle_invalid_args(self, args):
        if len(args) == 0:
            raise ZeroArgumentsError("uniq': wrong number of CL arguments")
        if len(args) == 2 and (args[0] != "-i" or args[0] != "<"):
            raise IncorrectFlagError("uniq: unknown flag" + args[0])
        if len(args) > 2:
            raise ExtraArgumentsError("uniq: extra commands" + args[2])

    def uniq_handle_two_args(self, file, consider_case):
        with open(file) as f:
            lines = f.readlines()
            # Handling the case when the file is empty
            if not lines:
                return self.out
            # Add the first line to 'self.out' as a starting
            # point for comparison
            self.out.append(lines[0])
            for i in range(1, len(lines)):
                if consider_case:
                    if lines[i].strip().lower() != \
                            self.out[-1].strip().lower():
                        self.out.append(lines[i])

    def uniq_handle_one_arg(self, file):

        with open(file) as f:
            lines = f.readlines()
            # Handling the case when the file is empty
            if not lines:
                return self.out
            # Add the first line to 'self.out' as a starting
            # point for comparison
            self.out.append(lines[0])
            for i in range(1, len(lines)):
                if lines[i].strip() != self.out[-1].strip():
                    self.out.append(lines[i])
