from collections import deque
import os
from .custom_exceptions import ZeroArgumentsError

'''
#Cat class
This class is used to read the contents of a file and print it to the screen

#Methods:
cat: Main method of the class, takes in a list of arguments and calls the
     cat_execute method if all arguments are valid.
cat_execute: Executes the cat command, takes in a list of arguments and
     prints the contents of the files.
cat_handle_invalid_args: Handles invalid arguments, throws an error if
     there are no arguments.
'''


class Cat():
    def __init__(self):
        self.out = deque()

    def cat(self, args, out1, checkBit):
        if len(args) == 0:
            self.cat_handle_invalid_args(args)
        # Cat can read a very large number of files,
        # so we do not need to check for a max number of args
        elif len(args) >= 1:
            # Ensure that all files exist and have read permissions
            for a in args:
                if not os.path.isfile(a.getText()):
                    raise FileNotFoundError("cat: " + a.getText() +
                                            ": No such file or directory")
            # If number of args and all files are valid, read them
            output = self.cat_execute(args, checkBit)
            return output

    def cat_execute(self, args, checkBit):
        # If checkBit is 0, we are not redirecting output
        listStrings = []
        for a in args:
            with open(a.getText()) as f:
                temp = f.read()
                if checkBit == 0:
                    self.out.append(temp)
                listStrings.append(temp)
        return listStrings

    def cat_handle_invalid_args(self, args):
        if len(args) == 0:
            raise ZeroArgumentsError("cat: missing arguments, "
                                     "add file names to read from")
