from collections import deque
import os
import codecs
from .custom_exceptions import (
    IncorrectFlagError,
    InsufficientArgumentsError,
    InvalidRangeError,
)

'''
The Cut class provides functionality similar to the Unix 'cut' command.
It is used for extracting sections from each line of files based
on byte position.

Attributes:
    out: A deque used for storing the output of the cut operation.

Methods:
    #cut:
    - Processes input arguments to determine file name and byte
      positions for extraction.
    - Includes error handling for incorrect argument number,
      wrong flags, and file access issues.
    - Orchestrates the overall execution flow by calling
      helper functions.

    #exec:
    - Main execution function that opens the specified file and
      calls print_file with proper arguments.
    - Raises InsufficientArgumentsError and IncorrectFlagError
      for argument validation.

    #print_file:
    - Reads the file and processes each line based on the specified
      byte intervals.
    - Calls print_bytes to handle the extraction of specified bytes
      from each line.

    #print_bytes:
    - Extracts and decodes the specified byte ranges from each line
      of the file.

    #process_intervals:
    - Processes the byte range argument into usable intervals.
    - Handles disjoint and overlapping intervals.

    #generate_intervals:
    - Generates a list of byte intervals from the given argument.
    - Sorts intervals for efficient processing.

    #check_value:
    - Parses and validates individual byte range values.
    - Raises InvalidRangeError if a range is invalid.

Exceptions:
    InsufficientArgumentsError: Raised if the number of arguments is
    incorrect.
    IncorrectFlagError: Raised if an incorrect flag is used.
    InvalidRangeError: Raised if the byte range specified is invalid
    or decreasing.
    FileNotFoundError: Raised if the specified file cannot be found
    or accessed.
'''


class Cut:
    def __init__(self):
        self.out = deque()

    def cut(self, args, out, checkBit):
        output = []
        args1 = []
        for x in args:
            # if isinstance(x, TerminalNodeImpl):
            #     continue
            # else:
            if type(x) != str:
                args1.append(x.getText())
            else:
                args1.append(x)

        def exec(args):
            if len(args) < 3:
                raise InsufficientArgumentsError(
                    "incorrect number of arguments"
                )
            else:
                # print("here")
                if args[0] != "-b":
                    raise IncorrectFlagError("wrong flag")
                cwd = os.getcwd()
                file_name = args[2]
                file_path = os.path.join(cwd, file_name)
                try:
                    with codecs.open(
                        file_path, "r", encoding="utf-8"
                    ) as file:
                        print_file(file, args)
                except IOError:
                    raise FileNotFoundError("can't find " + file_name)

        def print_file(file, args):
            length = os.path.getsize(file.name)
            intervals_out = process_intervals(args[1], length)
            for line in file:
                bytes = line.encode("utf-8")
                # print(bytes)
                # print(intervals_out)
                print_bytes(bytes, intervals_out)

        def print_bytes(bytes, intervals_out):
            # print(intervals_out)
            result = ""
            for interval in intervals_out:
                end = interval[1]
                if len(bytes) < interval[1]:
                    end = len(bytes)
                start = interval[0] - 1
                if len(bytes) < interval[0]:
                    start = len(bytes)
                add = bytes[start:end].decode("utf-8")
                # print(add)
                result += add.replace("\n", "")
                # output.append(add.replace("\n", ""))
            output.append(result)
            # print(output)

        def process_intervals(option, length):
            values = option.split(",")
            intervals = generate_intervals(values, option, length)
            disjoint = []
            last_byte = 0
            for interval in intervals:
                current = interval
                if current[1] > last_byte and current[0] < last_byte:
                    current = (last_byte + 1, current[1])
                    disjoint.append(current)
                    last_byte = current[1]
                elif current[0] > last_byte:
                    disjoint.append(current)
                    last_byte = current[1]
            return disjoint

        def generate_intervals(values, option, length):
            intervals = []
            for value in values:
                interval = check_value(value, option, length)
                intervals.append(interval)
            intervals.sort(key=lambda x: x[1])
            intervals.sort(key=lambda x: x[0])
            return intervals

        def check_value(value, option, length):
            # print(value)
            # print(option)
            # print(length)
            if "-" in value:
                i = value.index("-")
                first = value[:i]
                if first != "":
                    first = int(first)
                else:
                    first = 1
                second = value[i + 1:]
                if second != "":
                    second = int(second)
                else:
                    second = length
                # and each line interval is until /n reached
            else:
                first = int(value)
                second = first
            if second < first:
                raise InvalidRangeError("cut: invalid decreasing range")
            return (first, second)

        exec(args1)
        return output
