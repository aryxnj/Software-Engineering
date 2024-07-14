from antlr4 import CommonTokenStream
from antlr4 import InputStream
from antlr.antlrLexer import antlrLexer
from antlr.antlrParser import antlrParser
from ParserObserver import Parser
import re
import sys
import os
from collections import deque

'''
Main Shell Code

Functions:
    quoteText(text):
        - Processes a string to ensure proper quoting of statements within it.

    eval(cmdline, out):
        - Evaluates a given command line string.
        - Stores the output of the command in the provided deque.

Dependencies:
    - ANTLR4 for parsing command line input.
    - Custom ParserObserver for handling the parsed command tree.

Usage:
    - Can be run directly as a script for interactive command execution.
    - Accepts commands through command line arguments for direct execution.
'''


def quoteText(text):
    quoted_statements = []
    pattern = r"(?:(['\"`])(.*?)\1)"
    for match in re.finditer(pattern, text):
        quoted_statements.append(
            {
                "statement": match.group(0),
                "start_index": match.start(),
                "end_index": match.end(),
            }
        )
    lastIndex = 0
    newText = ""
    lastIndex = 0
    for x in quoted_statements:
        # print(text[x["end_index"]])
        if x["end_index"] == len(text):
            if text[x["start_index"] - 1] != " ":
                m = x["start_index"]
                while m >= 0 and text[m] != " ":
                    m -= 1
                newText += text[lastIndex: m + 1]
                newText += '"' + text[m + 1: x["end_index"]] + '"'
                lastIndex = x["end_index"]
        elif text[x["start_index"] - 1] != " " and text[x["end_index"]] != " ":
            n = x["end_index"]
            m = x["start_index"]
            while m >= 0 and text[m] != " ":
                m -= 1
            while n < len(text) and text[n] != " ":
                n += 1
            newText += text[lastIndex: m + 1]
            newText += '"' + text[m + 1: n] + '"'
            lastIndex = n
    newText += text[lastIndex:]
    if len(quoted_statements) == 0:
        return text
    return newText


def eval(cmdline, out):
    if (cmdline[0] == '"' and cmdline[-1] == '"' or
            cmdline[0] == "'" and cmdline[-1] == "'"):
        cmdline = cmdline[1:-1]
    space = cmdline.find(" ")
    args = cmdline[space + 1:]
    # print(args)
    if args[0] != '"' and args[-1] != '"' or \
       args[0] != '"' and args[-1] != '"':
        for x in range(len(cmdline)):
            if cmdline[x] == '"' or cmdline[x] == "`" or cmdline[x] == "'":
                if x > 0 and x < len(cmdline) - 1:
                    if cmdline[x - 1] != " ":
                        cmdline = quoteText(cmdline)
                        break
    input_stream = InputStream(cmdline)
    # out = deque()
    lexer = antlrLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = antlrParser(stream)
    tree = parser.a()
    listener = Parser(out)
    # walker = ParseTreeWalker()
    if tree.getChild(0).getRuleIndex() == 2:
        listener.enterSequence(tree.getChild(0))
    else:
        listener.enterCommand(tree.getChild(0))
    out = listener.out
    # out.extend(firstIter)


if __name__ == "__main__":
    args_num = len(sys.argv) - 1
    if args_num > 0:
        if args_num != 2:
            raise ValueError("wrong number of command line arguments")
        if sys.argv[1] != "-c":
            raise ValueError(f"unexpected command line argument {sys.argv[1]}")
        out = deque()
        eval(sys.argv[2], out)
        while len(out) > 0:
            print(out.popleft(), end="")
    else:
        while True:
            print(os.getcwd() + "> ", end="")
            cmdline = input()
            out = deque()
            eval(cmdline, out)
            while len(out) > 0:
                print(out.popleft(), end="")
