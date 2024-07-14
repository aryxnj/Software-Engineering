# Generated from antlrParser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .antlrParser import antlrParser
else:
    from antlrParser import antlrParser

# This class defines a complete listener for a parse tree produced by antlrParser.
class antlrParserListener(ParseTreeListener):

    # Enter a parse tree produced by antlrParser#a.
    def enterA(self, ctx:antlrParser.AContext):
        pass

    # Exit a parse tree produced by antlrParser#a.
    def exitA(self, ctx:antlrParser.AContext):
        pass


    # Enter a parse tree produced by antlrParser#command.
    def enterCommand(self, ctx:antlrParser.CommandContext):
        pass

    # Exit a parse tree produced by antlrParser#command.
    def exitCommand(self, ctx:antlrParser.CommandContext):
        pass


    # Enter a parse tree produced by antlrParser#sequence.
    def enterSequence(self, ctx:antlrParser.SequenceContext):
        pass

    # Exit a parse tree produced by antlrParser#sequence.
    def exitSequence(self, ctx:antlrParser.SequenceContext):
        pass


    # Enter a parse tree produced by antlrParser#redirection.
    def enterRedirection(self, ctx:antlrParser.RedirectionContext):
        pass

    # Exit a parse tree produced by antlrParser#redirection.
    def exitRedirection(self, ctx:antlrParser.RedirectionContext):
        pass


    # Enter a parse tree produced by antlrParser#redirectionSymbols.
    def enterRedirectionSymbols(self, ctx:antlrParser.RedirectionSymbolsContext):
        pass

    # Exit a parse tree produced by antlrParser#redirectionSymbols.
    def exitRedirectionSymbols(self, ctx:antlrParser.RedirectionSymbolsContext):
        pass


    # Enter a parse tree produced by antlrParser#globbing.
    def enterGlobbing(self, ctx:antlrParser.GlobbingContext):
        pass

    # Exit a parse tree produced by antlrParser#globbing.
    def exitGlobbing(self, ctx:antlrParser.GlobbingContext):
        pass


    # Enter a parse tree produced by antlrParser#quotation.
    def enterQuotation(self, ctx:antlrParser.QuotationContext):
        pass

    # Exit a parse tree produced by antlrParser#quotation.
    def exitQuotation(self, ctx:antlrParser.QuotationContext):
        pass


    # Enter a parse tree produced by antlrParser#simpleCommand.
    def enterSimpleCommand(self, ctx:antlrParser.SimpleCommandContext):
        pass

    # Exit a parse tree produced by antlrParser#simpleCommand.
    def exitSimpleCommand(self, ctx:antlrParser.SimpleCommandContext):
        pass


    # Enter a parse tree produced by antlrParser#pipe.
    def enterPipe(self, ctx:antlrParser.PipeContext):
        pass

    # Exit a parse tree produced by antlrParser#pipe.
    def exitPipe(self, ctx:antlrParser.PipeContext):
        pass


    # Enter a parse tree produced by antlrParser#argument.
    def enterArgument(self, ctx:antlrParser.ArgumentContext):
        pass

    # Exit a parse tree produced by antlrParser#argument.
    def exitArgument(self, ctx:antlrParser.ArgumentContext):
        pass


    # Enter a parse tree produced by antlrParser#identifier.
    def enterIdentifier(self, ctx:antlrParser.IdentifierContext):
        pass

    # Exit a parse tree produced by antlrParser#identifier.
    def exitIdentifier(self, ctx:antlrParser.IdentifierContext):
        pass



del antlrParser