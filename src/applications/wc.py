import os
from collections import deque
import codecs
from .custom_exceptions import (
    IncorrectFlagError,
    ExtraArgumentsError,
    ZeroArgumentsError,
)

'''
The wc class provides functionality similar to the Unix word count command.
It is used for counting the number of lines, words, and characters in files.

Attributes:
    out: A deque used for storing the output of the wc operation.

Methods:
    #wc:
    - Processes input arguments to determine the file and the counting mode
      (lines, words, characters).
    - Includes error handling for incorrect argument number and file access
      issues.
    - Orchestrates the overall execution flow by calling helper functions.

    #exec:
    - Main execution function that opens the specified file and determines
      which counting method to use.
    - Handles different flags (-l, -w, -c, -m) for counting lines, words,
      characters, and characters considering multibyte characters.
    - Raises ZeroArgumentsError, IncorrectFlagError, ExtraArgumentsError,
      and FileNotFoundError as appropriate.

    #print_file_line, #print_file_word, #print_file_char:
    - Count the number of lines, words, and characters in the file.
    - Append the count to the output.

    #print_file_line_two, #print_file_word_two, #print_file_char_two:
    - Similar to the above functions but return the count for use in
      cumulative calculations.

Exceptions:
    ZeroArgumentsError: Raised if no arguments are provided.
    IncorrectFlagError: Raised if an incorrect flag is used.
    ExtraArgumentsError: Raised if too many arguments are provided.
    FileNotFoundError: Raised if the specified file cannot be found
    or accessed.
'''


class Wc:
    def __init__(self):
        self.out = deque()

    def wc(self, args, out, checkBit):
        args1 = []
        output = []
        for x in args:
            # if isinstance(x, TerminalNodeImpl):
            #     continue
            # else:
            args1.append(x.getText())

        def exec(args):
            if len(args) == 0:
                raise ZeroArgumentsError("wrong number of arguments")
            if len(args) == 1:
                cwd = os.getcwd()
                file_name = args[0]
                file_path = os.path.join(cwd, file_name)
                try:
                    with codecs.open(
                        file_path, "r", encoding="utf-8"
                    ) as file:
                        print_file_line(file)
                except IOError:
                    raise FileNotFoundError("can't find " + file_name)
                try:
                    with codecs.open(
                        file_path, "r", encoding="utf-8"
                    ) as file:
                        print_file_word(file)
                except IOError:
                    raise FileNotFoundError("can't find " + file_name)
                try:
                    with codecs.open(
                        file_path, "r", encoding="utf-8"
                    ) as file:
                        print_file_char(file)
                except IOError:
                    raise FileNotFoundError("can't find " + file_name)
            elif len(args) == 2:
                if args[0] == "-l":
                    cwd = os.getcwd()
                    file_name = args[1]
                    file_path = os.path.join(cwd, file_name)
                    try:
                        with codecs.open(
                            file_path, "r", encoding="utf-8"
                        ) as file:
                            print_file_line(file)
                    except IOError:
                        raise FileNotFoundError("can't find " + file_name)
                elif args[0] == "-w":
                    cwd = os.getcwd()
                    file_name = args[1]
                    file_path = os.path.join(cwd, file_name)
                    try:
                        with codecs.open(
                            file_path, "r", encoding="utf-8"
                        ) as file:
                            print_file_word(file)
                    except IOError:
                        raise FileNotFoundError("can't find " + file_name)
                elif args[0] == "-c":
                    cwd = os.getcwd()
                    file_name = args[1]
                    file_path = os.path.join(cwd, file_name)
                    try:
                        with codecs.open(
                            file_path, "r", encoding="utf-8"
                        ) as file:
                            print_file_char(file)
                    except IOError:
                        raise FileNotFoundError("can't find " + file_name)
                elif args[0] == "-m":
                    cwd = os.getcwd()
                    file_name = args[1]
                    file_path = os.path.join(cwd, file_name)
                    try:
                        with codecs.open(
                            file_path, "r", encoding="utf-8"
                        ) as file:
                            print_file_char(file)
                    except IOError:
                        raise FileNotFoundError("can't find " + file_name)
                else:
                    raise IncorrectFlagError("wrong flag")
            elif len(args) == 3:
                if args[0] == "-l":
                    cwd = os.getcwd()
                    file_name = args[1]
                    file_path = os.path.join(cwd, file_name)
                    try:
                        with codecs.open(
                            file_path, "r", encoding="utf-8"
                        ) as file:
                            to_output = print_file_line_two(file)
                    except IOError:
                        raise FileNotFoundError("can't find " + file_name)
                    file_name = args[2]
                    file_path = os.path.join(cwd, file_name)
                    try:
                        with codecs.open(
                            file_path, "r", encoding="utf-8"
                        ) as file:
                            to_output_2 = print_file_line_two(file)
                            output.append(str(to_output + to_output_2))
                    except IOError:
                        raise FileNotFoundError("can't find " + file_name)

                elif args[0] == "-w":
                    cwd = os.getcwd()
                    file_name = args[1]
                    file_path = os.path.join(cwd, file_name)
                    try:
                        with codecs.open(
                            file_path, "r", encoding="utf-8"
                        ) as file:
                            to_output = print_file_word_two(file)
                    except IOError:
                        raise FileNotFoundError("can't find " + file_name)
                    file_name = args[2]
                    file_path = os.path.join(cwd, file_name)
                    try:
                        with codecs.open(
                            file_path, "r", encoding="utf-8"
                        ) as file:
                            to_output_2 = print_file_word_two(file)
                            output.append(str(to_output + to_output_2))
                    except IOError:
                        raise FileNotFoundError("can't find " + file_name)
                elif args[0] == "-c":
                    cwd = os.getcwd()
                    file_name = args[1]
                    file_path = os.path.join(cwd, file_name)
                    try:
                        with codecs.open(
                            file_path, "r", encoding="utf-8"
                        ) as file:
                            to_output = print_file_char_two(file)
                    except IOError:
                        raise FileNotFoundError("can't find " + file_name)
                    file_name = args[2]
                    file_path = os.path.join(cwd, file_name)
                    try:
                        with codecs.open(
                            file_path, "r", encoding="utf-8"
                        ) as file:
                            to_output_2 = print_file_char_two(file)
                            output.append(str(to_output + to_output_2))
                    except IOError:
                        raise FileNotFoundError("can't find " + file_name)
                elif args[0] == "-m":
                    cwd = os.getcwd()
                    file_name = args[1]
                    file_path = os.path.join(cwd, file_name)
                    try:
                        with codecs.open(
                            file_path, "r", encoding="utf-8"
                        ) as file:
                            to_output = print_file_char_two(file)
                    except IOError:
                        raise FileNotFoundError("can't find " + file_name)
                    file_name = args[2]
                    file_path = os.path.join(cwd, file_name)
                    try:
                        with codecs.open(
                            file_path, "r", encoding="utf-8"
                        ) as file:
                            to_output_2 = print_file_char_two(file)
                            output.append(str(to_output + to_output_2))
                    except IOError:
                        raise FileNotFoundError("can't find " + file_name)

            else:
                raise ExtraArgumentsError("Too many arguments")

        def print_file_line(file):
            count = 0
            for line in file:
                count += 1
            output.append(str(count))
            # print(count)

        def print_file_word(file):
            count = 0
            for line in file:
                count += len(line.split())
            output.append(str(count))
            # print(count)

        def print_file_char(file):
            count = 0
            for line in file:
                count += len(line)
            output.append(str(count))
            # print(count)

        def print_file_line_two(file):
            count = 0
            for line in file:
                count += 1
            return count
            # print(count)

        def print_file_word_two(file):
            count = 0
            for line in file:
                count += len(line.split())
            return count
            # print(count)

        def print_file_char_two(file):
            count = 0
            for line in file:
                count += len(line)
            return count
            # print(count)

        exec(args1)
        # print("out: ", output)
        # for line in output:
        #     self.out.append(line + "\n")
        return output
