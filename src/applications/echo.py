from collections import deque
from glob import glob

'''
Echo class

Attributes:
    out: Stores the output strings generated by the echo command.

Methods:
    echo:
    - Concatenates and processes input arguments, considering special
      characters and wildcard patterns.
    - Removes single and double quotes and expands wildcard patterns
      using globbing

Returns:
    string: The processed and concatenated string from the given arguments.

Notes:
    - The method handles wildcard characters ('*') by expanding them
      to match filenames.
    - Non-matching wildcard patterns are retained in the output.
'''


class Echo():
    def __init__(self):
        self.out = deque()

    def echo(self, args, out, checkBit):
        # Echo can take in a large number of arguments
        # and can also take in zero arguments,
        # so we do not need to check for a min/max number of args
        string1 = ""
        token = ""
        extended_tokens = []
        for token1 in args:
            if token1 is None:
                token = " "
            else:
                token = token1.getText()
            token = token.replace("'", "")
            token = token.replace('"', "")
            if "*" in token:
                globbed = glob(token)
                if globbed:  # If the glob pattern matches files
                    extended_tokens.extend(globbed)
                    for t in globbed:
                        string1 += t
                else:  # If no files match the glob pattern
                    extended_tokens.append(token)
                    for t in globbed:
                        string1 += t
            else:
                string1 += token + ""
                extended_tokens.append(token)
        if checkBit == 0:
            self.out.append(" ".join(extended_tokens) + "\n")
        string1 = " ".join(extended_tokens)
        return string1
