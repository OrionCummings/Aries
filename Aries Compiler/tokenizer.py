from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Self
from returns.result import Result, Success, Failure

class TokenType(Enum):
    NONE            = 0x00,
    EXIT            = 0x01,
    SEMICOLON       = 0x02,
    PAREN_OPEN      = 0x03,
    PAREN_CLOSE     = 0x04,
    BRACKET_OPEN    = 0x05,
    BRACKET_CLOSE   = 0x06,
    BRACE_OPEN      = 0x07,
    BRACE_CLOSE     = 0x08,
    COM_FSLASH      = 0x09,
    COM_HASH        = 0x0A,
    IDENTIFIER      = 0x0B,
    LIT_INT         = 0x10,
    LIT_UINT        = 0x11,
    LIT_CHAR        = 0x12,
    LIT_STR         = 0x13,
    LIT_BIN         = 0x14,
    LIT_OCT         = 0x15,
    LIT_HEX         = 0x16,
    OP_EQ           = 0x30,
    OP_PLUS         = 0x32,
    OP_MINUS        = 0x31,
    OP_STAR         = 0x33,
    OP_DIV          = 0x34,
    OP_MOD          = 0x35,
    OP_SHL          = 0x36,
    OP_SHR          = 0x37,
    OP_RHL          = 0x38,
    OP_RHR          = 0x39,
    OP_NOT          = 0x3A,
    OP_AND          = 0x3B,
    OP_OR           = 0x3C,
    OP_BITAND       = 0x3D,
    OP_BITOR        = 0x3E,
    OP_BITXOR       = 0x3F,
    CTRL_IF         = 0x70,
    CTRL_ELSE       = 0x71,
    CTRL_SWITCH     = 0x72,
    CTRL_CASE       = 0x73,
    CTRL_MATCH      = 0x74,
    CTRL_FOR        = 0x75,
    CTRL_WHILE      = 0x76

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
            case TokenType.LIT_INT:
                return ""
            case TokenType.LIT_UINT:
                return ""
            case TokenType.LIT_CHAR:
                return ""
            case TokenType.LIT_STR:
                return ""
            case TokenType.LIT_BIN:
                return ""
            case TokenType.LIT_OCT:
                return ""
            case TokenType.LIT_HEX:
                return ""
            case TokenType.OP_EQ:
                return "="
            case TokenType.OP_PLUS:
                return "+"
            case TokenType.OP_MINUS:
                return "-"
            case TokenType.OP_STAR:
                return "*"
            case TokenType.OP_DIV:
                return "/"
            case TokenType.OP_MOD:
                return "%"
            case TokenType.OP_SHL:
                return "<<"
            case TokenType.OP_SHR:
                return ">>"
            case TokenType.OP_RHL:
                return "<<<"
            case TokenType.OP_RHR:
                return ">>>"
            case TokenType.OP_NOT:
                return "!"
            case TokenType.OP_AND:
                return "&&"
            case TokenType.OP_OR:
                return "||"
            case TokenType.OP_BITAND:
                return "&"
            case TokenType.OP_BITOR:
                return "|"
            case TokenType.OP_BITXOR:
                return "^"
            case TokenType.CTRL_IF:
                return "if"
            case TokenType.CTRL_ELSE:
                return "else"
            case TokenType.CTRL_SWITCH:
                return "switch"
            case TokenType.CTRL_CASE:
                return "case"
            case TokenType.CTRL_MATCH:
                return "match"
            case TokenType.CTRL_FOR:
                return "for"
            case TokenType.CTRL_WHILE:
                return "while"
            case _:
                return "unknown"

@dataclass
class Token:
    Type: TokenType     = TokenType.NONE,
    Line: int           = 0,
    Value: str          = None

class Tokenizer():
    
    def __init__(Self, FilePath: str) -> Self:
        Self.Tokens: List[Token]    = []
        Self.Buffer: str            = ""
        Self.LineCount: int         = 0
        Self.FilePath: str          = FilePath
    
    def peek(): Optional[str]
    
    def Tokenize() -> Result[int, str]:
        
        CurrentLine: int = 1
        # return Failure('Some failure!')
        return Success(0)





