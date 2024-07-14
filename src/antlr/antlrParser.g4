parser grammar antlrParser;

options { tokenVocab= antlrLexer; }

a: command| sequence;
command : simpleCommand
        | command pipe simpleCommand
        | simpleCommand pipe simpleCommand
        | command pipe simpleCommand
        | simpleCommand pipe simpleCommand
        | redirection
        | command pipe redirection
        | command quotation
        | argument
        | (quotation)*
        ;
sequence: command Sequence command
        | sequence Sequence command
        ;
redirection: simpleCommand redirectionSymbols StringLiteral
            | Filename redirectionSymbols StringLiteral
            | redirection redirectionSymbols StringLiteral
            | redirectionSymbols StringLiteral command
            ;

redirectionSymbols: GreaterThan
                    | LessThan
                    ;

globbing: simpleCommand Asterisk simpleCommand
        | simpleCommand Asterisk argument
        | argument Asterisk simpleCommand
        | argument Asterisk argument
        ;
        
quotation: MULTIPLE_WORDS | QUOTED_STRING;

simpleCommand : identifier (argument) * 
              ;

pipe: PIPE;

argument : StringLiteral
         | Numbers
         | Identifier
         | Dot
         | Filename
         | Whitespace
         | Flag
         | quotation
         ;

identifier : Identifier ;