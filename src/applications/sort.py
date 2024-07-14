from collections import deque
from .custom_exceptions import InvalidArgumentsError

'''
The Sort class provides functionality similar to the Unix 'sort' command.
It is used for sorting the contents of a file.

Attributes:
    out: A deque used for storing the sorted output.

Methods:
    #sort:
    - Processes input arguments to determine the file and the sorting mode
      (normal or reverse).
    - Includes error handling for incorrect usage of arguments.
    - Reads the file, sorts its lines, and stores or returns the sorted
      lines based on checkBit.

    - If checkBit is 0, sorted lines are appended to 'out'.
    - If checkBit is 1, the sorted list is returned.

    - Handles the '-r' flag for reverse sorting.
    - Raises InvalidArgumentsError for incorrect usage of the command.

Exceptions:
    InvalidArgumentsError: Raised if the arguments are incorrect or used
    in the wrong way.
'''


class Sort:
    def __init__(self):
        self.out = deque()

    def sort(self, args, out, checkBit):
        # self.out = out
        # if len(args) != 1 and len(args) != 2:
        #     raise ValueError("wrong number of command line arguments")
        if len(args) == 0:
            # print("in args 0")
            return
        else:
            # print("args: ", len(args))
            if len(args) == 1:
                if type(args[0]) != str:
                    file = args[0].getText()
                else:
                    file = args[0]
                reverse_sort = False
            elif len(args) == 2 and args[0].getText() == "-r":
                file = args[1].getText()
                reverse_sort = True
            else:
                raise InvalidArgumentsError("sort: wrong usage")
            with open(file) as f:
                lines = f.readlines()
                sorted_lines = sorted(lines, reverse=reverse_sort)
                # print("list: ", sorted_lines)
                for line in sorted_lines:
                    if "\n" in line:
                        # line1 = line.replace('\n', '')
                        # print(line1)
                        if checkBit == 0:
                            self.out.append(line)
                    else:
                        # print(line)
                        if checkBit == 0:
                            self.out.append(line)
            # print("sorted_lines: ", sorted_lines)
            return sorted_lines
