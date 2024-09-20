from enum import Enum
from dataclasses import dataclass
import json
from typing import Dict, List, Optional, Self
from unicodedata import numeric
import returns
from returns.result import Result, Success, Failure
import unittest
import pprint

from Helpers import Debug, GetCurrentFunction

class TokenType(Enum):
    NONE                = 0x00,
    EXIT                = 0x01,
    SEMICOLON           = 0x02, # ;
    PAREN_OPEN          = 0x03, # (
    PAREN_CLOSE         = 0x04, # )
    BRACKET_OPEN        = 0x05, # [
    BRACKET_CLOSE       = 0x06, # ]
    BRACE_OPEN          = 0x07, # {
    BRACE_CLOSE         = 0x08, # }
    COM_FSLASH          = 0x09, # /
    COM_HASH            = 0x0A, # #
    IDENTIFIER          = 0x0B,
    RETURN_ARROW        = 0x0C, # ->
    KEYWORD_IF          = 0x70, # if
    KEYWORD_ELIF        = 0x71, # elif
    KEYWORD_ELSE        = 0x72, # else
    KEYWORD_WHILE       = 0x73, # while
    KEYWORD_FOR         = 0x74, # for
    KEYWORD_CONTINUE    = 0x75, # continue
    KEYWORD_OVERLOAD    = 0x76, # overload
    KEYWORD_RETURN      = 0x77, # return
    KEYWORD_VOID        = 0x78, # void
    KEYWORD_INT         = 0x79, # int
    KEYWORD_UINT        = 0x80, # uint
    KEYWORD_CHAR        = 0x81, # char
    KEYWORD_BOOL        = 0x82, # bool
    KEYWORD_FLOAT       = 0x83, # float
    KEYWORD_CONST       = 0x84, # const
    KEYWORD_STATIC      = 0x85, # static
    KEYWORD_MATCH       = 0x86, # match
    KEYWORD_SWITCH      = 0x87, # switch
    KEYWORD_CASE        = 0x88, # case
    KEYWORD_BREAK       = 0x89, # break
    KEYWORD_DEFAULT     = 0x8A, # default
    KEYWORD_ENUM        = 0x8B, # enum
    KEYWORD_DEF         = 0x8C, # def
    KEYWORD_STRUCT      = 0x8D, # struct
    KEYWORD_SIZEOF      = 0x8E, # sizeof
    KEYWORD_STD         = 0x8F, # std
    KEYWORD_CAST        = 0x90, # cast
    KEYWORD_ASM         = 0x91  # asm

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

KeywordMap: Dict[str, TokenType] = {
    "if": TokenType.KEYWORD_IF,
    "while": TokenType.KEYWORD_WHILE,
    "for": TokenType.KEYWORD_FOR,
    "continue": TokenType.KEYWORD_CONTINUE,
    "overload": TokenType.KEYWORD_OVERLOAD,
    "return": TokenType.KEYWORD_RETURN,
    "const": TokenType.KEYWORD_CONST,
    "static": TokenType.KEYWORD_STATIC,
    "match": TokenType.KEYWORD_MATCH,
    "switch": TokenType.KEYWORD_SWITCH,
    "case": TokenType.KEYWORD_CASE,
    "break": TokenType.KEYWORD_BREAK,
    "default": TokenType.KEYWORD_DEFAULT,
    "enum": TokenType.KEYWORD_ENUM,
    "def": TokenType.KEYWORD_DEF,
    "struct": TokenType.KEYWORD_STRUCT,
    "sizeof": TokenType.KEYWORD_SIZEOF,
    "std": TokenType.KEYWORD_STD,
    "cast": TokenType.KEYWORD_CAST,
    "asm": TokenType.KEYWORD_ASM
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
        Self.Buffer: str                   = ""
        Self.Tokens: List[Token]           = []
        Self.SourceFileContents: str       = None
        Self.SourceFileContentsLength: int = None
        
        # Open the source file
        with open(Self.FilePath) as SourceFile:
            Self.SourceFileContents = SourceFile.read()
        
        # Save the length for future calculations
        Self.SourceFileContentsLength: int = len(Self.SourceFileContents)
    
    def __str__(Self) -> str:
        return pprint.pformat(Self.__dict__)
    
    # Read some number of characters out of the source file
    def Peek(Self, NumCharacters: int = 1) -> Optional[str]:
        
        # If we are trying to read too many characters, return None
        if (Self.Index + NumCharacters) > Self.SourceFileContentsLength:
            return None
        
        # Return the requested character(s)
        Characters = Self.SourceFileContents[Self.Index:Self.Index + NumCharacters]
        return Characters
    
    def Pop(Self, NumCharacters: int = 1) -> Optional[str]:
        Characters = Self.Peek(NumCharacters)
        Self.Index += NumCharacters
        return Characters
    
    def ParseNext(Self) -> str:
        Buffer: str = ''
        while Self.Peek() and Self.Peek().isalnum():
            Buffer += Self.Pop()
        return Buffer
    
    def TokenizeNewline(Self, Buffer: str) -> int:
        return Self.LineCount + 1 if Buffer == "\n" else Self.LineCount
    
    def TokenizeKeywords(Self, Buffer: str) -> Result[TokenType, str]:
        return Success(KeywordMap[Buffer]) if Buffer in KeywordMap.keys() else Failure(Debug.Error() + "Failed to parse keyword '" + Buffer + "'!")
    
    def TokenizeCaptures(Self, Buffer: str) -> Result[TokenType, str]:
        match Buffer:
            case '(': return Success(TokenType.PAREN_OPEN)
            case ')': return Success(TokenType.PAREN_CLOSE)
            case '{': return Success(TokenType.BRACE_OPEN)
            case '}': return Success(TokenType.BRACE_CLOSE)
            case '[': return Success(TokenType.BRACKET_OPEN)
            case ']': return Success(TokenType.BRACKET_CLOSE)
            case _: return Failure("Unknown Capture '" + Buffer + "'!")
    
    def Tokenize(Self) -> Result[int, str]:
        
        # Intermediate buffer for building multi-character tokens
        Buffer: str = ""
        
        # While there are characters to read
        while Self.Peek() is not None:
            
            # If we can read an alphanumeric character
            if Self.Peek().isalnum():
                
                # Parse the next potential token
                Buffer = Self.ParseNext()
                
                # If the buffer contains only a new line, increment the line count
                Self.LineCount = Self.TokenizeNewline(Buffer)
                
                # Check the buffer for keywords
                Type = Self.TokenizeKeywords(Buffer)
                try:
                    Self.Tokens.append(Token(Type.unwrap(), Self.LineCount, None))
                except returns.primitives.exceptions.UnwrapFailedError:
                    Self.Tokens.append(Token(TokenType.IDENTIFIER, Self.LineCount, Buffer))
                except:
                    return Failure(Type.failure())
            
            elif Self.Peek() == '\n': # BUG: This may actually be two characters?
                Self.LineCount += 1
                Self.Pop()
                
            elif Self.Peek() == ';':
                Self.Tokens.append(Token(TokenType.SEMICOLON, Self.LineCount, None))
                Self.Pop()
            
            elif Self.Peek(2) == "->": # If we found a function return arrow
                Self.Tokens.append(Token(TokenType.RETURN_ARROW, Self.LineCount, None))
                Self.Pop(2)
                             
            elif Self.Peek(2) == "//": # If we found a singleline comment, pop the line
                while(not Self.Peek() == "\n"):
                    Self.Pop()
            
            elif Self.Peek(2) == "/*": # If we found a multiline comment, pop the line
                while(not Self.Peek() == "*/"):
                    Self.Pop()
            
            elif Self.Peek() == "(":
                Self.Tokens.append(Token(TokenType.PAREN_OPEN, Self.LineCount, None))
                Self.Pop()
                
            elif Self.Peek() == ")":
                Self.Tokens.append(Token(TokenType.PAREN_CLOSE, Self.LineCount, None))
                Self.Pop()
                
            elif Self.Peek() == "{":
                Self.Tokens.append(Token(TokenType.BRACE_OPEN, Self.LineCount, None))
                Self.Pop()
                
            elif Self.Peek() == "}":
                Self.Tokens.append(Token(TokenType.BRACE_CLOSE, Self.LineCount, None))
                Self.Pop()
                
            elif Self.Peek() == "[":
                Self.Tokens.append(Token(TokenType.BRACKET_OPEN, Self.LineCount, None))
                Self.Pop()
                
            elif Self.Peek() == "]":
                Self.Tokens.append(Token(TokenType.BRACKET_CLOSE, Self.LineCount, None))
                Self.Pop()
                    
            elif Self.Peek().isspace():
                Self.Pop()
                
            else:              
                return Failure(Debug.Error() + "Invalid token '" + Buffer + "'!")
        
            # Reset the buffer
            Buffer = ""
        
        return Success(0)

class TokenizerUnitTests(unittest.TestCase):
    
    def setUp(Self):
        pass

    def TestPeek(Self):
        pass
    
    def TestPop(Self):
        pass

    def TestTokenize(Self):
        pass