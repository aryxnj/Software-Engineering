from antlr4.tree.Tree import TerminalNodeImpl
from antlr4.tree.Tree import ParseTreeListener
from antlr.antlrLexer import antlrLexer
from antlr.antlrParser import antlrParser
from antlr4 import CommonTokenStream
from antlr4 import InputStream
from unsafeDecorator import UnsafeApplication
from applications.pwd import Pwd
from applications.cd import Cd
from applications.ls import Ls
from applications.echo import Echo
from applications.sort import Sort
from applications.head import Head
from applications.tail import Tail
from applications.grep import Grep
from applications.uniq import Uniq
from applications.cut import Cut
from applications.find import Find
from applications.sed import Sed
from applications.wc import Wc
import re

'''
-The `Parser` class is a custom implementation for parsing and executing
shell-like commands.
-It is designed to handle a sequence of commands and various command
types including built-in shell commands like 'pwd', 'cd', 'ls',
'echo', and others.

Attributes:
    checkbit1 (int): A flag used to handle specific parsing conditions.
    out: A deque used for storing the output of executed commands.
    checkbitPipe (int): A flag used to manage pipe ('|') operations
    within commands.

Methods:
    #enterSequence:
    - Processes a sequence of commands and manages their execution.
    - Handles the construction and execution flow of command sequences.

    #enterCommand:
    - Parses and executes individual commands within a sequence.
    - Handles redirection and pipe operations between commands.

    #pipeList1:
    - Manages the execution of commands that are piped together.
    - Directs the flow of output from one command to another as input.

    #enterSimpleCommand:
    - Executes simple commands without pipes or redirections.
    - Handles the execution of various shell commands by creating
      instances of corresponding classes.

    #enterRedirection:
    - Handles the redirection operations in shell commands
      (e.g., '>' and '<').

    #pipeOutputCommands:
    - Manages the output of commands when piped into other commands.
    - Responsible for passing the output of one command as input to
      another in a piped sequence.

This class leverages ANTLR4 for parsing and relies on custom
implementations of shell commands.
It acts as a listener to the parse tree and executes the
shell-like commands accordingly.
'''


@UnsafeApplication
def unsafeApp(checkBit):
    return


def addArgument(arg):
    cmdline = "ignore {}".format(arg)
    # print("cmdline: ", str(cmdline))
    input_stream = InputStream(cmdline)
    lexer = antlrLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = antlrParser(stream)
    tree = parser.simpleCommand()
    for x in tree.getChildren():
        # print(x.getRuleIndex())
        if x.getRuleIndex() != 10:
            return x

# Complete listener for a parse tree from parserTest.


class Parser(ParseTreeListener):
    def __init__(self, out):
        self.checkbit1 = 0
        self.out = out
        self.checkbitPipe = 0

    def enterSequence(self, ctx: antlrParser.SequenceContext, checkbit=0):
        # print("in here")
        global checkbit1
        self.checkbit1 = ctx.getChildCount()
        checkbit1 = self.checkbit1
        output = []
        for x in ctx.getChildren():
            # print("child: ", x.getRuleIndex())
            @UnsafeApplication
            def unsafeDecorator1(x):
                return

            unsafeDecorator1(x)
            if isinstance(x, TerminalNodeImpl):
                continue
            elif x.getRuleIndex() == 2:
                self.enterSequence(x, checkbit)
            elif x.getRuleIndex() == 1:
                # print("command text", x.getText())

                result = self.enterCommand(x, checkbit, 1)

                if result is not None:
                    output.append(result)
        # print("output Sequence: ", " ".join(output))
        return " ".join(output)

    # Enter a parse tree produced by parserTest#command.

    def enterCommand(
        self, ctx: antlrParser.CommandContext, checkbit=0, checkSequence=0
    ):
        # print("Entering Command:", ctx.getText())
        pipeList = []
        tempSave1 = []
        # print("children: ", ctx.getChildCount())
        for x in ctx.getChildren():
            tempSave1.append(x)
            # print("x: ", x.getRuleIndex())
        for y in range(len(tempSave1)):
            if tempSave1[y] is None:
                continue
            elif tempSave1[y].getRuleIndex() == 3:
                self.enterRedirection(x)
            elif tempSave1[y].getRuleIndex() == 8:
                # print("in pipe")
                self.checkbitPipe += 1
                pipeList = [tempSave1[y - 1], tempSave1[y + 1]]
                # newCommand.pop(y-1)
                # newCommand.append(pipeList)
                # print("checkbit2: ", str(checkbit2))
                return self.pipeList1(pipeList)
                # continue
            elif tempSave1[y].getRuleIndex() == 1:
                if y < len(tempSave1) - 1:
                    if isinstance(tempSave1[y], TerminalNodeImpl) is False:
                        if tempSave1[y + 1].getRuleIndex() == 6:
                            # print("in else 1")
                            for x in tempSave1[y].getChildren():
                                if x.getRuleIndex() == 7:
                                    tempChild = addArgument(
                                        tempSave1[y + 1].getText()
                                    )
                                    # print("tempChild: ", tempChild)
                                    x.addChild(tempChild)
                            output = self.enterCommand(tempSave1[y])
                else:
                    # print("else 2")
                    output = self.enterCommand(tempSave1[y])
                # newCommand.append(tempSave1[y])
                continue
            elif tempSave1[y].getRuleIndex() == 7:
                # print("in here")
                output = self.enterSimpleCommand(
                    tempSave1[y], checkbit, checkSequence
                )
                return output
                # newCommand.append(output)
                continue
            # except AttributeError as e:
            #     print("bdkjdnk")
            # newCommand.append(tempSave1[y])
        # for x in ctx.getChildren():
        #     # print("command child: ",x.getRuleIndex())
        #     if switch == 1:
        #         switch = 0
        #         pipeList.append(x)
        #         tempSave.append(pipeList)
        #         continue
        #     if x.getRuleIndex() == 3:
        #         enterRedirection(x)
        #     if x.getRuleIndex() == 9:
        #         print("in pipe")
        #         a = tempSave.pop()
        #         pipeList = [a]
        #         switch = 1
        #         continue
        #     elif x.getRuleIndex() == 1:
        #         output = self.enterCommand(x)
        #         tempSave.append(output)
        #     elif x.getRuleIndex() == 7:
        #         tempSave.append(x)
        #         continue
        #     tempSave.append(x)
        # # print("prev in Command: ", prev)
        # prev = "Command"
        # results = recurse(tempSave)
        # print("results: ", results)
        # return tempSave

    def pipeList1(self, list1):
        # print("pipe number: ", self.checkbitPipe)
        args = None
        if list1[0].getRuleIndex() == 1:
            # print("in list10")
            args = self.enterCommand(list1[0], 1)
            # print("args: ", args)
        if list1[1].getRuleIndex() == 3:
            for x in list1[1].getChildren():
                if x.getRuleIndex() == 7:
                    if args is not None:
                        tempChild = addArgument(args[0])
                        x.addChild(tempChild)
                    break
            return self.enterRedirection(list1[1])
        if list1[1].getRuleIndex() == 7:
            # print("in list11")
            # if args != None:
            #     tempChild = addArgument(args[0])
            #     list1[1].addChild(tempChild)
            return self.pipeOutputCommands(list1[1], args)

    def enterSimpleCommand(
        self, ctx: antlrParser.SimpleCommandContext, checkBit, checkSequence=0
    ):
        # if checkSequence == 1:
        #     print("in sequence")

        identifier = ctx.getChild(0).getText()
        # print("identifier: ", identifier)
        # for x in ctx.getChildren():
        # print("child: ", x.getText())
        args = []
        for x in ctx.getChildren():
            if isinstance(x, TerminalNodeImpl):
                args.append(x)
            elif x.getRuleIndex() != 10:
                if x.getRuleIndex() == 9 and x.getChildCount() >= 1:
                    if isinstance(x.getChild(0), TerminalNodeImpl) is False:
                        if x.getChild(0).getRuleIndex() == 6:
                            inputCommand = x.getChild(0).getText()
                            # print('before command: ', inputCommand)
                            if (
                                inputCommand[0] == "`"
                                and inputCommand[-1] == "`"
                            ):
                                inputCommand = inputCommand[1:-1]
                                input_stream = InputStream(inputCommand)
                                lexer = antlrLexer(input_stream)
                                stream = CommonTokenStream(lexer)
                                parser = antlrParser(stream)
                                tree = parser.a()
                                firstIter = None
                                listener = Parser(self.out)
                                # walker = ParseTreeWalker()
                                if tree.getChild(0).getRuleIndex() == 2:
                                    firstIter = listener.enterSequence(
                                        tree.getChild(0), 1
                                    )
                                else:
                                    firstIter = listener.enterCommand(
                                        tree.getChild(0), 1
                                    )
                                self.out = listener.out
                                if type(firstIter) == list:
                                    string1 = ""
                                    for x in firstIter:
                                        string1 += x
                                    # print(addArgument(string1).getText())
                                    args.append(addArgument(string1))
                                else:
                                    args.append(
                                        addArgument(str('"' + firstIter + '"'))
                                    )
                                    # print(firstIter)
                            else:

                                def find_backquote_indexes(inputCommand):
                                    pattern = r"`[^`]+`"
                                    matches = re.finditer(
                                        pattern, inputCommand
                                    )
                                    indexes = [
                                        (match.start(), match.end() - 1)
                                        for match in matches
                                    ]
                                    return indexes

                                if (
                                    len(find_backquote_indexes(inputCommand))
                                    > 0
                                ):
                                    backquote_indexes = find_backquote_indexes(
                                        inputCommand
                                    )
                                    backQuoteOutputs = []
                                    for i in backquote_indexes:
                                        command = inputCommand[i[0] + 1:i[1]]
                                        # print("in command: ", command, ")
                                        # print(inputCommand.find('`'))
                                        input_stream = InputStream(command)
                                        lexer = antlrLexer(input_stream)
                                        stream = CommonTokenStream(lexer)
                                        parser = antlrParser(stream)
                                        listener = Parser(self.out)
                                        tree = parser.a()
                                        firstIter = listener.enterCommand(
                                            tree.getChild(0), 1
                                        )
                                        firstIter = None
                                        if (
                                            tree.getChild(0).getRuleIndex()
                                            == 2
                                        ):
                                            firstIter = listener.enterSequence(
                                                tree.getChild(0), 1
                                            )
                                        else:
                                            firstIter = listener.enterCommand(
                                                tree.getChild(0), 1
                                            )
                                            self.out = listener.out
                                        # print("firstIter: ", firstIter)
                                        backQuoteOutputs.append(firstIter)
                                    lastIndex = 1
                                    newArgsString = ""
                                    n = 0
                                    for i in backquote_indexes:
                                        newArgsString += (
                                            inputCommand[lastIndex:i[0]]
                                            + backQuoteOutputs[n]
                                        )
                                        lastIndex = i[1] + 1
                                        n += 1
                                    newArgsString += inputCommand[lastIndex:-1]
                                    # print("newString: ", newArgsString)
                                    args.append(
                                        addArgument(
                                            str('"' + newArgsString + '"')
                                        )
                                    )
                                    # print("concat: ", ))
                                else:
                                    # args.append()
                                    args.append(x)
                        else:
                            # print("x0: ", x.getText())
                            args.append(x)
                    else:
                        args.append(x)
                else:
                    # print("x2: ", x.getText())
                    args.append(x)
            # for x in args:
            # print("child: ", x.getText())
            # print("x: ", x.getText())
            # if x.getRuleIndex() != 11:
        if identifier == "pwd":
            pwdHandler = Pwd()
            output = pwdHandler.pwd(args, self.out, checkBit)
            self.out.extend(pwdHandler.out)
            return output
        elif identifier == "cd":
            cdHandler = Cd()
            output = cdHandler.cd(args, self.out, checkBit)
            self.out.extend(cdHandler.out)
            return output
        elif identifier == "ls":
            lsHandler = Ls()
            output = lsHandler.ls(args, self.out, checkBit)
            self.out.extend(lsHandler.out)
            return output
        elif identifier == "echo":
            echoHandler = Echo()
            output = echoHandler.echo(args, self.out, checkBit)
            self.out.extend(echoHandler.out)
            return output
        elif identifier == "cat":
            listStrings = []
            for a in args:
                # print("Attempting to open:", a)  # Debugging line
                if type(a) != str:
                    temp = a.getText()
                else:
                    temp = a
                with open(temp) as f:
                    # print(f.read())
                    temp = f.read()
                    temp = "\n".join(temp.splitlines()) + "\n"
                    if checkBit == 0:
                        #     # print("in cat out")
                        self.out.append(temp)
                    listStrings.append(temp)
            # print("listStrings: ", listStrings)
            # print("out cat: ", str(out))
            return listStrings
        elif identifier == "sort":
            sortHandler = Sort()
            output = sortHandler.sort(args, self.out, checkBit)
            self.out.extend(sortHandler.out)
            # print("output: ", output)
            return output
        elif identifier == "head":
            headHandler = Head()
            output = headHandler.head(args, self.out, checkBit)
            self.out.extend(headHandler.out)
            return output
        elif identifier == "tail":
            tailHandler = Tail()
            output = tailHandler.tail(args, self.out, checkBit)
            self.out.extend(tailHandler.out)
            return output
        elif identifier == "grep":
            grepHandler = Grep()
            output = grepHandler.grep(args, self.out, checkBit)
            self.out.extend(grepHandler.out)
            return output
            # if len(args) < 2:
            #     raise ValueError("wrong number of command line arguments")
        elif identifier == "uniq":
            # print("uniq simpleCommand")
            uniqHandler = Uniq()
            output = uniqHandler.uniq(args, self.out, checkBit)
            self.out.extend(uniqHandler.out)
            self.out.append("\n")
            return output
        elif identifier == "cut":
            cutHandler = Cut()
            output = cutHandler.cut(args, self.out, checkBit)
            for line in output:
                self.out.append(line + "\n")
            return output
            # print(result)
        elif identifier == "find":
            findHandler = Find()
            output = findHandler.find(args, self.out, checkBit)
            # print(checkBit)
            # self.out = findHandler.out
            if checkBit == 0:
                for line in output:
                    # print("output: ", line)
                    self.out.append(line + "\n")
            return output
        elif identifier == "sed":
            # print("in sed")
            sedHandler = Sed()
            output = sedHandler.sed(args, self.out, checkBit)
            # self.out.extend(sedHandler.out)
            # print("output: ", output)
            for line in output:
                # print("output: ", line)
                self.out.append(line)
            return output
        elif identifier == "wc":
            # print("in wc")
            wcHandler = Wc()
            output = wcHandler.wc(args, self.out, checkBit)
            # self.out.extend(sedHandler.out)
            # print("output: ", output)
            for line in output:
                # print("output: ", line)
                self.out.append(line + "\n")
            return output
        else:
            unsafeApp(checkSequence)

    def enterRedirection(self, ctx: antlrParser.RedirectionContext):
        global checkbit1
        # print("in redirection")
        children = []
        textChildren = []
        for x in ctx.getChildren():
            result = x
            textChildren.append(x.getText())
            children.append(result)

        n = 0
        # for x in children:
        #     if isinstance(x, TerminalNodeImpl):
        #         continue
        #     else:
        #         if x.getRuleIndex() == 4:
        # print("in redirec symbols: ", x.getText())
        while n < len(children):
            # print(type(children[n]))
            # try:
            if isinstance(children[n], TerminalNodeImpl):
                # print("here: ", children[n].getText())
                n += 1
                continue
            elif (
                children[n].getRuleIndex() == 4
                and children[n].getText() == ">"
            ):
                if n == 0:
                    if len(children) == 3:
                        if (
                            isinstance(children[n + 1], TerminalNodeImpl)
                            and children[n + 2].getRuleIndex() == 11
                        ):
                            file = open(children[n + 1].getText(), "w")
                            file.writelines(children[n + 2].getText())
                            file.close()
                            n += 3
                        elif (
                            isinstance(children[n + 1], TerminalNodeImpl)
                            and children[n + 2].getRuleIndex() == 1
                        ):
                            tempChild = addArgument(children[n + 1])
                            for x in children[n + 2].getChildren():
                                if x.getRuleIndex() == 7:
                                    x.addChild(tempChild)
                            self.enterSimpleCommand(children[n + 2], 0)
                            n += 3
                elif children[n - 1].getRuleIndex() == 7:
                    # print("here1")
                    # for y in children[n - 1].getChildren():
                    # if y.getRuleIndex() == 12:
                    # if y.getText() == "echo" and checkbit1 <= 1:
                    #     # print("here")
                    #     tempCheckbit = 0
                    # else:
                    #     tempCheckbit = 1
                    args = self.enterSimpleCommand(children[n - 1], 1)
                    # print("args list: ", args)
                    tempList = args
                    # if type(args) == str:
                    #     with open(args) as f:
                    #         tempList.append(f.read())
                    # else:
                    #     for x in args:
                    #         if type(x) != str:
                    #             x = x.getText()
                    #         # print("x", x)
                    #         with open(x) as f:
                    #             tempList.append(f.read())
                    # print("tempList", str(tempList))
                    # print("tempList: ", tempList)
                    # print("token number: ", children[n + 1].getRuleIndex())
                    # print("tmpList: ", tempList)
                    file = open(children[n + 1].getText(), "w")
                    file.writelines(tempList)
                    file.close()
            elif (
                children[n].getRuleIndex() == 4
                and children[n].getText() == "<"
            ):
                if children[n - 1].getRuleIndex() == 7:
                    # print(str(children[n+1]))
                    tempChild = addArgument(children[n + 1].getText())
                    # print("tempChild: ",tempChild)
                    children[n - 1].addChild(tempChild)
                    # print("newChild text: ", children[n - 1].getText())
                    # for x in children[n-1].getChildren():
                    #     # print("node text: ", x.getText())
                    self.enterSimpleCommand(children[n - 1], 0)
                else:
                    for x in children[n - 1].getChildren():
                        if x.getRuleIndex() == 7:
                            tempChild = addArgument(children[n + 1])
                            # print("tempChild1: ", tempChild)
                            x.addChild(tempChild)
                            # print("newChild in loop", x.getChildCount())
                            self.enterSimpleCommand(x, 0)
                            break
            n += 1
            # children[n - 1].addChild(tempChild)
            # newChild = children[n - 1]
            # for x in newChild.getChildren():
            # print(x.getText())
            # except AttributeError as e:
            #     print(f"AttributeError 1: {e}")
            # n += 1

    def pipeOutputCommands(
        self,
        ctx: antlrParser.SimpleCommandContext,
        outputFromCommand,
        checkBit=0,
    ):
        identifier = ctx.getChild(0).getText()
        # print("identifier: ", identifier)
        args = []
        for x in ctx.getChildren():
            if isinstance(x, TerminalNodeImpl):
                args.append(x)
            elif x.getRuleIndex() != 10:
                args.append(x)
        if identifier == "grep":
            if type(outputFromCommand) == list:
                # print("in pipe grep")
                # print("args: ", str(args))
                pattern = args[0].getText().replace("'", "")
                # print(pattern)
                # print("output1: ", outputFromCommand)
                for x in outputFromCommand:
                    # print("x1: ", x)
                    # print("x: ", x)
                    z = x.split("\n")
                    # print("z: ", str(z))
                    for q in z:
                        if re.match(pattern, q):
                            # print("shell: ", q)
                            self.out.append(q + "\n")
        elif identifier == "cat":
            listStrings = []
            if len(outputFromCommand) != 0:
                file = open("temp.txt", "w")
                file.writelines(outputFromCommand)
                file.close()
                args = ["temp.txt"]
            for a in args:
                if type(a) != str:
                    temp = a.getText()
                else:
                    temp = a
                with open(temp) as f:
                    # print(f.read())
                    temp = f.read()
                    temp = "\n".join(temp.splitlines()) + "\n"
                    if checkBit == 0:
                        #     # print("in cat out")
                        self.out.append(temp)
                    listStrings.append(temp)
            # print("listStrings: ", listStrings)
            # print("out cat: ", str(out))
            return listStrings
        elif identifier == "uniq":
            # print("uniq simpleCommand")
            # print("in uniq pipe")
            # print("input in uniq: ", outputFromCommand)
            args1 = []
            for x in args:
                # if isinstance(x, TerminalNodeImpl):
                #     continue
                # else:
                args1.append(x)
            output = []
            file = open("temp.txt", "w")
            file.writelines(outputFromCommand)
            file.close()
            args1.append("temp.txt")

            # print(args1)
            uniqHandler = Uniq()
            output = uniqHandler.uniq(args1, self.out, checkBit)
            self.out.extend(uniqHandler.out)
            self.out.append("\n")
            return output

        elif identifier == "cut":
            output = []
            args1 = []
            for x in args:
                # if isinstance(x, TerminalNodeImpl):
                #     continue
                # else:
                args1.append(x)
            output = []
            file = open("temp.txt", "w")
            file.writelines(outputFromCommand)
            file.close()

            args1.append("temp.txt")
            cutHandler = Cut()
            output = cutHandler.cut(args1, self.out, checkBit)
            for line in output:
                self.out.append(line + "\n")
            return output

        elif identifier == "sort":
            # print("in sort pipe number: ", self.checkbitPipe)
            # print("output: ", outputFromCommand)
            # print("checkbit2 in sort: ", checkbit2)
            file = open("temp.txt", "w")
            file.writelines(outputFromCommand)
            file.close()
            args.append("temp.txt")
            sortHandler = Sort()
            output = sortHandler.sort(args, self.out, checkBit)
            if self.checkbitPipe <= 1:
                self.out.extend(sortHandler.out)
            # print("output: ", output)
            return output
        elif identifier == "head":
            file = open("temp.txt", "w")
            file.writelines(outputFromCommand)
            file.close()
            args.append("temp.txt")
            # print(args)
            headHandler = Head()
            output = headHandler.head(args, self.out, checkBit)
            self.out.extend(headHandler.out)
            return output
        elif identifier == "tail":
            file = open("temp.txt", "w")
            file.writelines(outputFromCommand)
            file.close()
            args.append("temp.txt")
            tailHandler = Tail()
            output = tailHandler.tail(args, self.out, checkBit)
            self.out.extend(tailHandler.out)
            return output
