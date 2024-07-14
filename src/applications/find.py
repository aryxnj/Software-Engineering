from collections import deque
import os
from .custom_exceptions import (
    ExtraArgumentsError,
    InsufficientArgumentsError,
    IncorrectFlagError,
)

'''
The Find class provides functionality similar to the Unix 'find' command.
It is used for searching for files in a directory hierarchy.

Attributes:
    out: A deque used for storing the output of the find operation.

Methods:
    #find:
    - Processes input arguments to determine search criteria and paths.
    - Includes error handling for incorrect argument number, unknown
      flags, and specific argument requirements.
    - Orchestrates the overall execution flow by calling helper functions.

    #exec:
    - Main execution function that handles the search logic based on the
      provided arguments.

    #handle_invalid_args:
    - Checks for and handles cases of invalid or insufficient arguments.
    - Raises InsufficientArgumentsError, IncorrectFlagError, and
      ExtraArgumentsError as appropriate.

    #check_valid_args:
    - Validates and processes the correct arguments for the search
      operation.

    #handle_zero_args, #handle_one_arg, #handle_app_args:
    - Handle specific argument scenarios, such as no arguments, one
      argument, or application arguments.

    #get_all_target_files, #check_targets_matching:
    - Searches for files matching specific patterns or criteria.

    #get_specific_file_path, #get_all_file_paths:
    - Implements the logic for traversing directories and listing
      files based on the search criteria.

Exceptions:
    InsufficientArgumentsError: Raised if the number of arguments are
    insufficient.
    IncorrectFlagError: Raised if an incorrect or unknown flag is used.
    ExtraArgumentsError: Raised if there are extraneous arguments.
    FileNotFoundError: Raised if the specified directory or file cannot
    be found or accessed.
'''


class Find:
    def __init__(self):
        self.out = deque()

    def find(self, args, out, checkBit):
        args1 = []
        for x in args:
            # if isinstance(x, TerminalNodeImpl):
            #     continue
            # else:
            args1.append(x.getText())
            # print("x: ", x.getText())
        output = []

        def exec(args):
            current_wd = os.getcwd()
            handle_invalid_args(args)
            check_valid_args(args, current_wd)

        def handle_invalid_args(args):
            if len(args) == 2 and args[1] == "-name":
                raise InsufficientArgumentsError(
                    "find: missing argument to " + args[1]
                )
            if len(args) == 3 and args[1] != "-name":
                raise IncorrectFlagError("find: unknown predicate " + args[1])
            if len(args) > 3:
                raise ExtraArgumentsError(
                    "paths must preceed expression " + args[-1]
                )

        def check_valid_args(args, current_wd):
            if len(args) == 0:
                handle_zero_args(current_wd)
            elif len(args) == 1:
                handle_one_arg(args)
            elif len(args) == 2 and args[0] == "-name":
                handle_app_args(current_wd, 2, ".", args[1])
            elif len(args) == 3:
                handle_app_args(current_wd, 3, args[0], args[2])
            else:
                raise IncorrectFlagError("find: unknown predicate " + args[1])

        def handle_zero_args(current_wd):
            initial_string = "."
            get_all_file_paths(current_wd, initial_string)

        def handle_one_arg(args):
            initial_string = args[0]
            get_all_file_paths(args[0], initial_string)

        def handle_app_args(current_wd, size, initial_string, file_target):
            if size == 3:
                if "*" in file_target:
                    file_target = file_target.replace("'", "")
                    # print("in glob")
                    targets = file_target.split("*")
                    get_all_target_files(
                        initial_string, initial_string, targets
                    )
                else:
                    get_specific_file_path(
                        current_wd, initial_string, file_target
                    )
            else:
                if "*" in file_target:
                    # print("in glob1")
                    file_target = file_target.replace("'", "")
                    # print("file_target: ", file_target)
                    targets = file_target.split("*")
                    get_all_target_files(current_wd, initial_string, targets)
                else:
                    get_specific_file_path(
                        current_wd, initial_string, file_target
                    )

        def get_all_target_files(current_wd, initial_string, targets):
            list_of_files = os.listdir(current_wd)
            for file_name in list_of_files:
                if check_targets_matching(file_name, targets):
                    output.append(initial_string + "/" + file_name)
                if os.path.isdir(current_wd + "/" + file_name):
                    new_relative_path = initial_string + "/" + file_name
                    next_dir = current_wd + "/" + file_name
                    get_all_target_files(next_dir, new_relative_path, targets)

        def check_targets_matching(file_name, targets):
            for target in targets:
                if target not in file_name:
                    return False
            return True

        def get_specific_file_path(current_wd, initial_string, target):
            list_of_files = os.listdir(current_wd)
            for file_name in list_of_files:
                if file_name == target:
                    output.append(initial_string + "/" + file_name)
                if os.path.isdir(current_wd + "/" + file_name):
                    new_relative_path = initial_string + "/" + file_name
                    next_dir = current_wd + "/" + file_name
                    get_specific_file_path(
                        next_dir, new_relative_path, target
                    )

        def get_all_file_paths(current_wd, initial_string):
            list_of_files = os.listdir(current_wd)
            for file_name in list_of_files:
                if os.path.isdir(current_wd + "/" + file_name):
                    new_relative_path = initial_string + os.sep + file_name
                    next_dir = current_wd + os.sep + file_name
                    get_all_file_paths(next_dir, new_relative_path)
                output.append(initial_string + os.sep + file_name)

        exec(args1)
        return output
