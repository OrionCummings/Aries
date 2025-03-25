from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, List, Optional
from option import Err, Ok, Result

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
    TYPE_INT                = auto(), # int
    TYPE_CHAR               = auto(), # char
    TYPE_STRING             = auto(), # string
    TYPE_BOOL               = auto(), # bool
    TYPE_FLOAT              = auto(), # float

    def __str__(type) -> str:

        if isinstance(type, TokenType):
            return type.name
        else:
            return "unknown"

keywordDictionary: Dict[str, TokenType] = {
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

puncutationDictionary: Dict[str, TokenType] = {
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

operatorDictionary: Dict[str, TokenType] = {
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
    type: TokenType      = TokenType.NONE,
    line: int            = 0,
    value: Optional[str] = None

class Tokenizer():
    
    def __init__(self, file_path: str):
        self.file_path: str                   = file_path
        self.index: int                       = 0
        self.line_count: int                  = 1
        self.tokens: List[Token]              = []
        self.source_file_contents: str        = None
        self.source_file_contents_length: int = None
    
    def __str__(self) -> str:

        builder: str = ""

        for token in self.tokens:
            builder += str(token)

        return builder
    
    def setup(self):

        # Open the source file
        with open(self.file_path) as source_file:
            self.source_file_contents = source_file.read()
        
        # Save the length for future calculations
        self.source_file_contents_length: int = len(self.source_file_contents)

        # Save the total number of lines for future calculations
        self.source_file_contents_num_lines: int = len(self.source_file_contents.splitlines())

    def peek(self, num_characters: int = 1) -> Optional[str]:
        
        # If we are trying to read an invalid number of characters, return None
        if num_characters < 1:
            return None
        
        # If we are trying to read too many characters, return None
        if (self.index + num_characters) > self.source_file_contents_length:
            return None
        
        # Return the requested character(s)
        characters = self.source_file_contents[self.index:self.index + num_characters]
        return characters
    
    def pop(self, num_characters: int = 1) -> Optional[str]:
        characters = self.peek(num_characters)
        
        if characters is None:
            return None
        
        self.index += num_characters
        return characters
    
    def parse_next(self) -> str:
        buffer: str = ''
        while self.peek() and self.peek().isalnum():
            buffer += self.pop()
        return buffer
    
    def process_newline(self, buffer: str) -> int:
        return self.line_count + 1 if buffer == "\n" else self.line_count
    
    # TODO: This doesn't need to be in this class. Static maybe? 
    def tokenize_keywords(self, buffer: str) -> Optional[TokenType]:
        return keywordDictionary[buffer] if buffer in keywordDictionary else None

    def parse_operators(self) -> Optional[str]:
        """Parses an operator at the current parsing head. Returns None on failure."""
        
        for N in [3,2,1]:
            peek = self.peek(N)
            if peek in operatorDictionary:
                return peek

        return None
    
    def tokenize(self) -> Result[None, str]:
        
        # Intermediate buffer for building multi-character tokens
        buffer: str = ""
        
        # While there are characters to read
        while self.peek() is not None:

            # Collect alphanumeric characters into a buffer
            while self.peek().isalnum():
                buffer += self.pop()

            # When a non-alphanumeric character is 
            # found, the identifier is complete

            if keyword := self.tokenize_keywords(buffer):
                self.tokens.append(keyword)
            else:
                self.tokens.append(Token(TokenType.IDENTIFIER, None, buffer))

            pass
        
        # Add an EOF to the end
        self.tokens.append(Token(TokenType.EOF, self.source_file_contents_num_lines, None))

        return Ok(self.tokens)

if __name__ == "__main__":

    source_file_dir = "C:\\Users\\Orion\\Stash\\PersonalProjects\\Aries\\Compiler\\C Compiler (x86 Target)\\Source Files"
    source_file_name = "ReturnZero.c"
    source_file_path = source_file_dir + "\\" + source_file_name

    t = Tokenizer(source_file_path)
    t.setup()
    t.tokenize()

    print(t)




