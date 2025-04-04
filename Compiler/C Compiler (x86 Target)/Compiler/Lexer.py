from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, List, Optional
from option import Err, Ok, Result

class TokenType(Enum):
    NONE                    = auto(),
    EXIT                    = auto(),
    IDENTIFIER              = auto(),
    LITERAL                 = auto(),
    EOF                     = auto(),
    SYM_SEMICOLON           = auto(), # ;
    SYM_COLON               = auto(), # :
    SYM_COMMA               = auto(), # ,
    SYM_QUESTION            = auto(), # ?
    SYM_FSLASH              = auto(), # /
    SYM_PAREN_OPEN          = auto(), # (
    SYM_PAREN_CLOSE         = auto(), # )
    SYM_BRACKET_OPEN        = auto(), # [
    SYM_BRACKET_CLOSE       = auto(), # ]
    SYM_BRACE_OPEN          = auto(), # {
    SYM_BRACE_CLOSE         = auto(), # }
    SYM_EQUAL               = auto(), # =
    SYM_PLUS                = auto(), # +
    SYM_DASH                = auto(), # -
    SYM_SLASH               = auto(), # /
    SYM_STAR                = auto(), # *
    SYM_PERCENT             = auto(), # %
    SYM_EXCLAIM             = auto(), # !
    SYM_LT                  = auto(), # <
    SYM_GT                  = auto(), # >
    SYM_AMPERSAND           = auto(), # &
    SYM_PIPE                = auto(), # |
    SYM_CARRET              = auto(), # ^
    SYM_SQUOTE              = auto(), # '
    SYM_DQUOTE              = auto(), # "
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
    KEYWORD_CAST            = auto(), # as
    KEYWORD_ASM             = auto(), # asm
    KEYWORD_NEW             = auto(), # new
    KEYWORD_TRUE            = auto(), # true
    KEYWORD_FALSE           = auto(), # false
    KEYWORD_INT             = auto(), # int
    KEYWORD_UINT            = auto(), # uint
    KEYWORD_FLOAT           = auto(), # float
    KEYWORD_CHAR            = auto(), # char
    KEYWORD_STRING          = auto(), # string
    KEYWORD_VOID            = auto(), # void

    def __str__(type) -> str:

        if isinstance(type, TokenType):
            return type.name
        else:
            return "unknown"

keyword_dictionary: Dict[str, TokenType] = {
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
    "int":          TokenType.KEYWORD_INT,
    "uint":         TokenType.KEYWORD_UINT,
    "float":        TokenType.KEYWORD_FLOAT,
    "char":         TokenType.KEYWORD_CHAR,
    "string":       TokenType.KEYWORD_STRING,
    "void":         TokenType.KEYWORD_VOID,
}

symbol_dictionary: Dict[str, TokenType] = {
    ";":  TokenType.SYM_SEMICOLON,
    ":":  TokenType.SYM_COLON,
    ",":  TokenType.SYM_COMMA,
    "?":  TokenType.SYM_QUESTION,
    "(":  TokenType.SYM_PAREN_OPEN,
    ")":  TokenType.SYM_PAREN_CLOSE,
    "{":  TokenType.SYM_BRACE_OPEN,
    "}":  TokenType.SYM_BRACE_CLOSE,
    "[":  TokenType.SYM_BRACKET_OPEN,
    "]":  TokenType.SYM_BRACKET_CLOSE,
    "=":  TokenType.SYM_EQUAL,
    "+":  TokenType.SYM_PLUS,
    "-":  TokenType.SYM_DASH,
    "/":  TokenType.SYM_SLASH,
    "*":  TokenType.SYM_STAR,
    "%":  TokenType.SYM_PERCENT,
    "!":  TokenType.SYM_EXCLAIM,
    "<":  TokenType.SYM_LT,
    ">":  TokenType.SYM_GT,
    "&":  TokenType.SYM_AMPERSAND,
    "|":  TokenType.SYM_PIPE,
    "^":  TokenType.SYM_CARRET,
    "\'": TokenType.SYM_SQUOTE,
    "\"": TokenType.SYM_DQUOTE,
}

pair_symbol_list = [
    "\'",
    "\"",
]

def is_keyword(sequence: str) -> Optional[TokenType]:
    return keyword_dictionary[sequence] if sequence in keyword_dictionary else None

def is_symbol(sequence: str) -> Optional[TokenType]:
    return symbol_dictionary[sequence] if sequence in symbol_dictionary else None

def is_identifier(sequence: str) -> Optional[TokenType]:

        # A valid identifier is a sequence of characters 
        # that begins with an alphabetical character and 
        # contains any alphanumeric or valid symbolic character.
        # Valid identifiers match with the following regex:
        # \b[A-Za-z_][A-Za-z0-9_]*
        # ^    ^         ^       ^
        # |    |         |       |
        # | begins with an alphabetical character
        # |              |       |
        # |        followed by any alphanumeric or valid symbolic character...
        # must be on a           |
        # word boundary   ...repeated any number of times
        #                     (including zero times!)
        #
        # With this being said, regex is not used here (or anywhere in
        # this lexer) because it is overkill. We will just follow
        # python's default identifer check

        return TokenType.IDENTIFIER if sequence.isidentifier() else None

def is_literal(sequence: str) -> Optional[TokenType]:

    if sequence == '': return None

    if is_literal_integer_token_type := is_literal_integer(sequence):
        return is_literal_integer_token_type
    if is_literal_float_token_type   :=  is_literal_float(sequence):
        return is_literal_float_token_type
    if is_literal_char_token_type    :=  is_literal_char(sequence):
        return is_literal_char_token_type
    if is_literal_string_token_type  :=  is_literal_string(sequence):
        return is_literal_string_token_type
    if is_literal_bool_token_type    :=  is_literal_bool(sequence):
        return is_literal_bool_token_type
    
    return None

def is_literal_integer(sequence: str) -> Optional[TokenType]:

    rules = [

        # Must be numeric
        sequence.isnumeric()
    ]

    return TokenType.LITERAL if all(rules) else None

def is_literal_float(sequence: str) -> Optional[TokenType]:

    rules = [

        # Must end with 'f'
        sequence[-1] == 'f', 

        # If one f and one period are replaced, the number must be numeric
        sequence.replace('f', '', count=1).replace('.', '', count=1).isnumeric()
    ]
    
    return TokenType.LITERAL if any(rules) else None

def is_literal_char(sequence: str) -> Optional[TokenType]:

    # TODO: This will fail because of a lack of short circuit evaluation!
    # What if len(sequence) < 3?
    rules = [

        # Must be three characters total (' x ')
        len(sequence) == 3,

        # Must start and end with single quotes
        sequence[0] == "\'" and sequence[2] == "\'",

        # The center symbol must be a valid character
        sequence[1].isalpha()
    ]

    return TokenType.LITERAL if all(rules) else None

def is_literal_string(sequence: str) -> Optional[TokenType]:

    rules = [

        # Must start and end with double quotes
        sequence[0] == "\"" and sequence[-1] == "\"" 
    ]

    return TokenType.LITERAL if all(rules) else None
    
def is_literal_bool(sequence: str) -> Optional[TokenType]:

    rules = [
        sequence == "0",
        sequence == "1",
        sequence == "true",
        sequence == "false",
    ]
    
    return TokenType.LITERAL if any(rules) else None

def is_pair_symbol(sequence: str) -> bool:
    return bool(sequence in pair_symbol_list)

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

        intermediate = []

        for token in self.tokens:
            intermediate.append(str(token))

        return ", \n".join(intermediate)
    
    def test(self, expected_tokens):

        equal = True

        for i in range(0, len(self.tokens)):

            print(self.tokens[i], end=" ")

            if i < len(expected_tokens) and self.tokens[i] != expected_tokens[i]:
                print(f"!= {expected_tokens[i]}")
                equal = False
            else:
                print()

        print()
        print("equal") if equal else print("not equal")

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

        buffer: str = ""

        # If there is a character to read
        if peek := self.peek():

            # If this character is a space, consume it
            if peek.isspace():
                self.pop()

            # If this character is alphanumeric
            elif peek.isalnum():

                # While this character is alphanumeric, 
                # build a buffer out of it.
                while self.peek().isalnum():
                    buffer += self.pop()

            # If this character is not alphanumeric
            elif not peek.isalnum():

                if is_symbol(peek):
                    buffer += self.pop()
                else:
                    # TODO: Make this a real error!
                    print(f"ERROR: '{peek}' not identifiable!")
                    self.pop()

        return buffer

    # TODO: Use later
    def process_newline(self, buffer: str) -> int:
        return self.line_count + 1 if buffer == "\n" else self.line_count
    
    def tokenize(self) -> Result[None, str]:
        
        # Intermediate buffer for building multi-character tokens
        buffer: str = ""
        
        # While there are characters to read
        while self.peek() is not None:

            buffer = self.parse_next()
            pass

            # DEBUG:
            if buffer == "\"":
                pass

            # If the buffer is a space or it's empty, then
            # we can't do anything.
            if buffer.isspace() or buffer == '':
                continue

            # Is the buffer a single quote?
            elif buffer == "\'":
                    
                full_char_sequence = "\'" + self.pop(2)

                if is_literal_char(full_char_sequence):

                    # Remove the quotes and add to the token list
                    buffer = full_char_sequence[1:-1]
                    self.tokens.append(Token(TokenType.LITERAL, None, buffer))

            # Is the buffer a double quote?
            elif buffer == "\"":

                # Find the right hand double quote
                while self.peek() != "\"":

                    # Consume everything
                    buffer += self.pop()

                # If the next character doesn't exist, then we failed to
                # close this string literal!
                if self.peek() == None:
                    print("failed to close string literal!")
                    exit(123)

                buffer += self.pop()

                # Remove the first character (which should be a double quote)
                buffer = buffer[1:-1]

                # Add the literal token to the token list
                self.tokens.append(Token(TokenType.LITERAL, None, buffer))

            # Is the buffer a valid symbol?
            elif token_type := is_symbol(buffer):
                self.tokens.append(Token(token_type, None, None))

            # Is the buffer a valid keyword?
            elif token_type := is_keyword(buffer):
                self.tokens.append(Token(token_type, None, None))

            # Is the buffer a valid identifier?
            elif token_type := is_identifier(buffer):
                self.tokens.append(Token(token_type, None, buffer))

            # Is the buffer a valid literal?
            elif token_type := is_literal(buffer):
                self.tokens.append(Token(token_type, None, buffer))

            # Otherwise, ...?
            else:

                pass
        
        # Add an EOF to the end
        self.tokens.append(Token(TokenType.EOF, None, None))

        return Ok(self.tokens)

if __name__ == "__main__":

    source_file_dir = "C:\\Users\\Orion\\Stash\\PersonalProjects\\Aries\\Compiler\\C Compiler (x86 Target)\\Source Files"
    # source_file_name = "ReturnLiteralInteger.c"
    # source_file_name = "ReturnLiteralString.c"
    source_file_name = "ReturnLiteralCharacter.c"
    source_file_path = source_file_dir + "\\" + source_file_name

    expected_token_list_return_literal_integer = [
        Token(TokenType.KEYWORD_INT, None, None),
        Token(TokenType.IDENTIFIER, None, "main"),
        Token(TokenType.SYM_PAREN_OPEN, None, None),
        Token(TokenType.KEYWORD_INT, None, None),
        Token(TokenType.IDENTIFIER, None, "argc"),
        Token(TokenType.SYM_COMMA, None, None),
        Token(TokenType.KEYWORD_CHAR, None, None),
        Token(TokenType.SYM_STAR, None, None),
        Token(TokenType.SYM_STAR, None, None),
        Token(TokenType.IDENTIFIER, None, "argv"),
        Token(TokenType.SYM_PAREN_CLOSE, None, None),
        Token(TokenType.SYM_BRACE_OPEN, None, None),
        Token(TokenType.KEYWORD_RETURN, None, None),
        Token(TokenType.LITERAL, None, "0"),
        Token(TokenType.SYM_SEMICOLON, None, None),
        Token(TokenType.SYM_BRACE_CLOSE, None, None),
        Token(TokenType.EOF, None, None),
    ]

    expected_token_list_return_literal_string = [
        Token(TokenType.KEYWORD_CHAR, None, None),
        Token(TokenType.SYM_STAR, None, None),
        Token(TokenType.IDENTIFIER, None, "test"),
        Token(TokenType.SYM_PAREN_OPEN, None, None),
        Token(TokenType.SYM_PAREN_CLOSE, None, None),
        Token(TokenType.SYM_BRACE_OPEN, None, None),
        Token(TokenType.KEYWORD_RETURN, None, None),
        Token(TokenType.LITERAL, None, "test string @ $#**()}!"),
        Token(TokenType.SYM_SEMICOLON, None, None),
        Token(TokenType.SYM_BRACE_CLOSE, None, None),
        Token(TokenType.EOF, None, None),
    ]

    expected_token_list_return_literal_character = [
        Token(TokenType.KEYWORD_CHAR, None, None),
        Token(TokenType.IDENTIFIER, None, "test"),
        Token(TokenType.SYM_PAREN_OPEN, None, None),
        Token(TokenType.SYM_PAREN_CLOSE, None, None),
        Token(TokenType.SYM_BRACE_OPEN, None, None),
        Token(TokenType.KEYWORD_RETURN, None, None),
        Token(TokenType.LITERAL, None, "g"),
        Token(TokenType.SYM_SEMICOLON, None, None),
        Token(TokenType.SYM_BRACE_CLOSE, None, None),
        Token(TokenType.EOF, None, None),
    ]

    t = Tokenizer(source_file_path)
    t.setup()
    t.tokenize()
    
    print()
    
    t.test(expected_token_list_return_literal_character)




