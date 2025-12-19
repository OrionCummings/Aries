from enum import Enum, auto
from dataclasses import dataclass
import string
from typing import Dict, List, Optional, Self
import returns
from returns.result import Result, Success, Failure
import unittest
import pprint

from Helpers import Debug

class TokenType(Enum):
    NONE                    = auto(),
    EXIT                    = auto(),
    IDENTIFIER              = auto(),
    EOF                     = auto(),
    ARROW                   = auto(), # ->
    PUNC_SEMICOLON          = auto(), # ;
    PUNC_COLON              = auto(), # :
    PUNC_COMMA              = auto(), # ,
    PUNC_QUESTION           = auto(), # ?
    PUNC_FSLASH             = auto(), # /
    PUNC_PAREN_OPEN         = auto(), # (
    PUNC_PAREN_CLOSE        = auto(), # )
    PUNC_BRACKET_OPEN       = auto(), # [
    PUNC_BRACKET_CLOSE      = auto(), # ]
    PUNC_BRACE_OPEN         = auto(), # {
    PUNC_BRACE_CLOSE        = auto(), # }
    KEYWORD_IF              = auto(), # if
    KEYWORD_ELIF            = auto(), # elif
    KEYWORD_ELSE            = auto(), # else
    KEYWORD_WHILE           = auto(), # while
    KEYWORD_FOR             = auto(), # for
    KEYWORD_CONTINUE        = auto(), # continue
    KEYWORD_OVERLOAD        = auto(), # overload
    KEYWORD_RETURN          = auto(), # return
    KEYWORD_CONST           = auto(), # const
    KEYWORD_STATIC          = auto(), # static
    KEYWORD_MATCH           = auto(), # match
    KEYWORD_SWITCH          = auto(), # switch
    KEYWORD_CASE            = auto(), # case
    KEYWORD_BREAK           = auto(), # break
    KEYWORD_DEFAULT         = auto(), # default
    KEYWORD_ENUM            = auto(), # enum
    KEYWORD_DEF             = auto(), # def
    KEYWORD_STRUCT          = auto(), # struct
    KEYWORD_SIZEOF          = auto(), # sizeof
    KEYWORD_TYPEOF          = auto(), # typeof
    KEYWORD_STD             = auto(), # std
    KEYWORD_CAST            = auto(), # as
    KEYWORD_ASM             = auto(), # asm
    KEYWORD_NEW             = auto(), # new
    KEYWORD_TRUE            = auto(), # true
    KEYWORD_FALSE           = auto(), # false
    OP_PLUS                 = auto(), # +
    OP_DASH                 = auto(), # -
    OP_SLASH                = auto(), # /
    OP_STAR                 = auto(), # *
    OP_PERCENT              = auto(), # %
    OP_EQUIVALENCE          = auto(), # ==
    OP_NONEQUIVALENCE       = auto(), # !=
    OP_NOT                  = auto(), # !
    OP_LT                   = auto(), # <
    OP_LTE                  = auto(), # <=
    OP_GT                   = auto(), # >
    OP_GTE                  = auto(), # >=
    OP_AND                  = auto(), # &&
    OP_OR                   = auto(), # ||
    OP_BIT_AND              = auto(), # &
    OP_BIT_OR               = auto(), # |
    OP_BIT_XOR              = auto(), # ^
    OP_INC                  = auto(), # ++
    OP_DEC                  = auto(), # --
    OP_ADD_ASSIGN           = auto(), # +=
    OP_SUB_ASSIGN           = auto(), # -=
    OP_MUL_ASSIGN           = auto(), # *=
    OP_DIV_ASSIGN           = auto(), # /=
    OP_MOD_ASSIGN           = auto(), # %=
    OP_ASSIGNMENT           = auto(), # =
    OP_SL                   = auto(), # <<
    OP_SR                   = auto(), # >>
    OP_RL                   = auto(), # <<<
    OP_RR                   = auto(), # >>>

    def __str__(type: Self) -> str:
        match type:
            case TokenType.EXIT:
                return "exit"
            case TokenType.SEMICOLON:
                return ";"
            case TokenType.PAREN_OPEN:
                return "("
            case TokenType.PAREN_CLOSE:
                return ")"
            case TokenType.BRACKET_OPEN:
                return "["
            case TokenType.BRACKET_CLOSE:
                return "]"
            case TokenType.BRACE_OPEN:
                return "{"
            case TokenType.BRACE_CLOSE:
                return "}"
            case TokenType.COM_FSLASH:
                return "/"
            case TokenType.COM_HASH:
                return "#"
            case TokenType.IDENTIFIER:
                return "identifier"
            case TokenType.RETURN_ARROW:
                return "->"
            case TokenType.KEYWORD_DEF:
                return "def"
            case TokenType.KEYWORD_IF:
                return "if"
            case TokenType.KEYWORD_ELSE:
                return "else"
            case TokenType.KEYWORD_SWITCH:
                return "switch"
            case TokenType.KEYWORD_CASE:
                return "case"
            case TokenType.KEYWORD_MATCH:
                return "match"
            case TokenType.KEYWORD_FOR:
                return "for"
            case TokenType.KEYWORD_WHILE:
                return "while"
            case _:
                return "unknown"

KeywordDictionary: Dict[str, TokenType] = {
    "if":           TokenType.KEYWORD_IF,
    "while":        TokenType.KEYWORD_WHILE,
    "for":          TokenType.KEYWORD_FOR,
    "continue":     TokenType.KEYWORD_CONTINUE,
    "match":        TokenType.KEYWORD_MATCH,
    "switch":       TokenType.KEYWORD_SWITCH,
    "case":         TokenType.KEYWORD_CASE,
    "break":        TokenType.KEYWORD_BREAK,
    "default":      TokenType.KEYWORD_DEFAULT,
    
    "def":          TokenType.KEYWORD_DEF,
    "struct":       TokenType.KEYWORD_STRUCT,
    "enum":         TokenType.KEYWORD_ENUM,
    "overload":     TokenType.KEYWORD_OVERLOAD,
    "const":        TokenType.KEYWORD_CONST,
    "static":       TokenType.KEYWORD_STATIC,
    
    "return":       TokenType.KEYWORD_RETURN,
    
    "sizeof":       TokenType.KEYWORD_SIZEOF,
    "typeof":       TokenType.KEYWORD_TYPEOF,
    
    "as":           TokenType.KEYWORD_CAST,
    
    "asm":          TokenType.KEYWORD_ASM,
    
    "new":          TokenType.KEYWORD_NEW,
    
    "true":         TokenType.KEYWORD_TRUE,
    "false":        TokenType.KEYWORD_FALSE,
}

PuncutationDictionary: Dict[str, TokenType] = {
    ";": TokenType.PUNC_SEMICOLON,
    ":": TokenType.PUNC_COLON,
    
    ",": TokenType.PUNC_COMMA,
    
    "?": TokenType.PUNC_QUESTION,
    
    "/": TokenType.PUNC_FSLASH,
    
    "(": TokenType.PUNC_PAREN_OPEN,
    ")": TokenType.PUNC_PAREN_CLOSE,
    
    "{": TokenType.PUNC_BRACE_OPEN,
    "}": TokenType.PUNC_BRACE_CLOSE,
    
    "[": TokenType.PUNC_BRACKET_OPEN,
    "]": TokenType.PUNC_BRACKET_CLOSE,
}

OperatorDictionary: Dict[str, TokenType] = {
    "+":            TokenType.OP_PLUS,
    "-":            TokenType.OP_DASH,
    "/":            TokenType.OP_SLASH,
    "*":            TokenType.OP_STAR,
    "%":            TokenType.OP_PERCENT,
    
    "=":            TokenType.OP_ASSIGNMENT,
    
    "==":           TokenType.OP_EQUIVALENCE,
    "!=":           TokenType.OP_NONEQUIVALENCE,
    "!":            TokenType.OP_NOT,
    "<":            TokenType.OP_LT,
    "<=":           TokenType.OP_LTE,
    ">":            TokenType.OP_GT,
    ">=":           TokenType.OP_GTE,
    "&&":           TokenType.OP_AND,
    "||":           TokenType.OP_OR,
    
    "&":            TokenType.OP_BIT_AND,
    "|":            TokenType.OP_BIT_OR,
    "^":            TokenType.OP_BIT_XOR,
    "<<":           TokenType.OP_SL,
    ">>":           TokenType.OP_SR,
    "<<<":          TokenType.OP_RL,
    ">>>":          TokenType.OP_RR,
    
    "+=":           TokenType.OP_ADD_ASSIGN,
    "-=":           TokenType.OP_SUB_ASSIGN,
    "*=":           TokenType.OP_MUL_ASSIGN,
    "/=":           TokenType.OP_DIV_ASSIGN,
    "%=":           TokenType.OP_MOD_ASSIGN,
    
    "++":           TokenType.OP_INC,
    "--":           TokenType.OP_DEC,
}

@dataclass
class Token:
    Type: TokenType      = TokenType.NONE,
    Line: int            = 0,
    Value: Optional[str] = None

class Tokenizer():
    
    def __init__(Self, FilePath: str) -> Self:
        Self.FilePath: str                 = FilePath
        Self.Index: int                    = 0
        Self.LineCount: int                = 1
        Self.Tokens: List[Token]           = []
        Self.SourceFileContents: str       = None
        Self.SourceFileContentsLength: int = None
        
        # Open the source file
        with open(Self.FilePath) as SourceFile:
            Self.SourceFileContents = SourceFile.read() #.translate(str.maketrans('', '', string.whitespace))
        
        # Save the length for future calculations
        Self.SourceFileContentsLength: int = len(Self.SourceFileContents)
    
    def __str__(Self) -> str:
        return pprint.pformat(Self.__dict__)
    
    def Peek(Self, NumCharacters: int = 1) -> Optional[str]:
        
        # if we are trying to read an invalid number of characters, return None
        if NumCharacters < 1:
            return None
        
        # If we are trying to read too many characters, return None
        if (Self.Index + NumCharacters) > Self.SourceFileContentsLength:
            return None
        
        # Return the requested character(s)
        Characters = Self.SourceFileContents[Self.Index:Self.Index + NumCharacters]
        return Characters
    
    def Pop(Self, NumCharacters: int = 1) -> Optional[str]:
        Characters = Self.Peek(NumCharacters)
        
        if Characters is None:
            return None
        
        Self.Index += NumCharacters
        return Characters
    
    def ParseNext(Self) -> str:
        Buffer: str = ''
        while Self.Peek() and Self.Peek().isalnum():
            Buffer += Self.Pop()
        return Buffer
    
    def ProcessNewline(Self, Buffer: str) -> int:
        return Self.LineCount + 1 if Buffer == "\n" else Self.LineCount
    
    def TokenizeKeywords(Self, Buffer: str) -> Optional[TokenType]:
        return KeywordDictionary[Buffer] if Buffer in KeywordDictionary else None
    
    def ParseOperators(Self) -> Optional[str]:
        """Parses an operator at the current parsing head. Returns None on failure."""
        
        for N in [3,2,1]:
            Peek = Self.Peek(N)
            if Peek in OperatorDictionary:
                return Peek

        return None
    
    def Tokenize(Self) -> Result[int, str]:
        
        # Intermediate buffer for building multi-character tokens
        Buffer: str = ""
        
        # While there are characters to read
        while Self.Peek() is not None:
            
            # If we can read an alphanumeric character
            if Self.Peek().isalnum():
                
                # Parse the next potential token
                Buffer = Self.ParseNext()
                
                # Check for float literals with a '.'!!!
                # BUG: Does not work properly lol!
                if Self.Peek() == '.':
                    Buffer += Self.Pop()
                    Buffer += Self.ParseNext()
                
                # If the buffer contains only a new line, increment the line count
                Self.LineCount = Self.ProcessNewline(Buffer)
                
                # Check the buffer for keywords
                Type = Self.TokenizeKeywords(Buffer)
                if Type is not None:
                    Self.Tokens.append(Token(Type, Self.LineCount, None))
                else:
                    Self.Tokens.append(Token(TokenType.IDENTIFIER, Self.LineCount, Buffer))
            
            elif Self.Peek() == '"': # Found a double quote => string start (arbitrary length)
                Buffer += Self.Pop()
                while Self.Peek() != '"':
                    Buffer += Self.Pop()
                Buffer += Self.Pop()
                Self.Tokens.append(Token(TokenType.IDENTIFIER, Self.LineCount, Buffer))
            
            elif Self.Peek() == "'": # Found a single quote => char start (a single character!)
                Buffer += Self.Pop()
                while Self.Peek() != "'":
                    Buffer += Self.Pop()
                Buffer += Self.Pop()
                Self.Tokens.append(Token(TokenType.IDENTIFIER, Self.LineCount, Buffer))
            
            elif Self.Peek() == '\n': # BUG: This may actually be two characters?
                Self.LineCount += 1
                Self.Pop()
                
            elif Self.Peek() == ',':
                Self.Tokens.append(Token(TokenType.PUNC_COMMA, Self.LineCount, None))
                Self.Pop()
            
            elif Self.Peek(2) == "->": # If we found an arrow
                Self.Tokens.append(Token(TokenType.ARROW, Self.LineCount, None))
                Self.Pop(2)
            
            elif Self.Peek(2) == "//": # If we found a single line comment, pop the line
                while(not Self.Peek() == "\n"):
                    Self.Pop()
            
            elif Self.Peek(2) == "/*": # If we found a multiline comment, pop the line
                while(not Self.Peek() == "*/"):
                    Self.Pop()
            
            elif (Peek := Self.ParseOperators()) is not None:
                Self.Tokens.append(Token(OperatorDictionary[Peek], Self.LineCount, None))
                Self.Pop(len(Peek))
            
            elif (Peek := Self.Peek()) in PuncutationDictionary:
                Self.Tokens.append(Token(PuncutationDictionary[Peek], Self.LineCount, None))
                Self.Pop()
            
            elif Self.Peek() == None: # TODO: I don't think this will ever work
                Self.Tokens.append(Token(TokenType.EOF, Self.LineCount, None))
            
            elif Self.Peek().isspace():
                Self.Pop()
            
            else:
                return Failure(Debug.Error() + "Invalid token '" + Buffer + "'!")

            # Reset the buffer
            Buffer = ""
        
        Self.Tokens.append(Token(TokenType.EOF, Self.LineCount, None))
        
        return Success(0)

