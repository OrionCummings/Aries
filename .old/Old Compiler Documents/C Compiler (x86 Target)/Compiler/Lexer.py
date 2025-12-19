from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, List, Optional
from option import Err, Ok, Result

class TokenType(Enum):
    NONE                    = auto(),
    IDENTIFIER              = auto(),
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
    SYM_CARET               = auto(), # ^
    SYM_SQUOTE              = auto(), # '
    SYM_DQUOTE              = auto(), # "
    LIT_INT                 = auto(), # integers
    LIT_UINT                = auto(), # unsigned integers
    LIT_FLOAT               = auto(), # floats
    LIT_CHAR                = auto(), # characters
    LIT_STRING              = auto(), # strings
    KEYWORD_BOOL            = auto(), # bool
    KEYWORD_BREAK           = auto(), # break
    KEYWORD_CASE            = auto(), # case
    KEYWORD_CHAR            = auto(), # char
    KEYWORD_CONST           = auto(), # const
    KEYWORD_CONTINUE        = auto(), # continue
    KEYWORD_DEFAULT         = auto(), # default
    KEYWORD_ELSE            = auto(), # else
    KEYWORD_ENUM            = auto(), # enum
    KEYWORD_FLOAT           = auto(), # float
    KEYWORD_FOR             = auto(), # for
    KEYWORD_IF              = auto(), # ir
    KEYWORD_INT             = auto(), # int
    KEYWORD_NULLPTR         = auto(), # nullptr
    KEYWORD_RETURN          = auto(), # return
    KEYWORD_SIZEOF          = auto(), # sizeof
    KEYWORD_STATIC          = auto(), # static
    KEYWORD_STRUCT          = auto(), # struct
    KEYWORD_SWITCH          = auto(), # switch
    KEYWORD_TYPEDEF         = auto(), # typedef
    KEYWORD_UNSIGNED        = auto(), # unsigned
    KEYWORD_VOID            = auto(), # void
    KEYWORD_WHILE           = auto(), # while

    def __str__(type) -> str:

        if isinstance(type, TokenType):
            return type.name
        else:
            return "unknown"

keyword_dictionary: Dict[str, TokenType] = {
    "bool":         TokenType.KEYWORD_BOOL,
    "break":        TokenType.KEYWORD_BREAK,
    "case":         TokenType.KEYWORD_CASE,
    "char":         TokenType.KEYWORD_CHAR,
    "const":        TokenType.KEYWORD_CONST,
    "continue":     TokenType.KEYWORD_CONTINUE,
    "default":      TokenType.KEYWORD_DEFAULT,
    "else":         TokenType.KEYWORD_ELSE,
    "enum":         TokenType.KEYWORD_ENUM,
    "float":        TokenType.KEYWORD_FLOAT,
    "for":          TokenType.KEYWORD_FOR,
    "if":           TokenType.KEYWORD_IF,
    "int":          TokenType.KEYWORD_INT,
    "nullptr":      TokenType.KEYWORD_NULLPTR,
    "return":       TokenType.KEYWORD_RETURN,
    "sizeof":       TokenType.KEYWORD_SIZEOF,
    "static":       TokenType.KEYWORD_STATIC,
    "struct":       TokenType.KEYWORD_STRUCT,
    "switch":       TokenType.KEYWORD_SWITCH,
    "typedef":      TokenType.KEYWORD_TYPEDEF,
    "unsigned":     TokenType.KEYWORD_UNSIGNED,
    "void":         TokenType.KEYWORD_VOID,
    "while":        TokenType.KEYWORD_WHILE,
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
    "/":  TokenType.SYM_FSLASH,
    "*":  TokenType.SYM_STAR,
    "%":  TokenType.SYM_PERCENT,
    "!":  TokenType.SYM_EXCLAIM,
    "<":  TokenType.SYM_LT,
    ">":  TokenType.SYM_GT,
    "&":  TokenType.SYM_AMPERSAND,
    "|":  TokenType.SYM_PIPE,
    "^":  TokenType.SYM_CARET,
    "\'": TokenType.SYM_SQUOTE,
    "\"": TokenType.SYM_DQUOTE,
}

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
    if is_literal_unsigned_integer_token_type :=  is_literal_unsigned_integer(sequence):
        return is_literal_unsigned_integer_token_type
    if is_literal_float_token_type :=  is_literal_float(sequence):
        return is_literal_float_token_type
    if is_literal_char_token_type :=  is_literal_char(sequence):
        return is_literal_char_token_type
    if is_literal_string_token_type :=  is_literal_string(sequence):
        return is_literal_string_token_type
    
    return None

def is_literal_integer(sequence: str) -> Optional[TokenType]:

    rules = [

        # Must be numeric
        sequence.isnumeric()
    ]

    return TokenType.LIT_INT if all(rules) else None

def is_literal_unsigned_integer(sequence: str) -> Optional[TokenType]:

    disqualifying_rules = [
        len(sequence) == 0
    ]
    
    if any(disqualifying_rules): return None

    rules = [
        sequence[0:-1].isdecimal(),
        sequence[-1] == 'u'
    ]
    
    return TokenType.LIT_UINT if all(rules) else None

def is_literal_float(sequence: str) -> Optional[TokenType]:

    rules = [

        # Must end with 'f'
        sequence[-1] == 'f', 

        # If one f and one period are replaced, the number must be numeric
        sequence.replace('f', '', count=1).replace('.', '', count=1).isnumeric()
    ]
    
    return TokenType.LIT_FLOAT if all(rules) else None

def is_literal_char(sequence: str) -> Optional[TokenType]:

    # This is a special check for empty character literals!
    if sequence == "''":
        return TokenType.LIT_CHAR

    disqualifying_rules = [
        len(sequence) < 3
    ]
    
    if any(disqualifying_rules): return None

    rules = [

        # Must be three characters
        len(sequence) == 3,

        # The first and third characters must be single quotes
        sequence[0] == "\'" and sequence[2] == "\'",

        # The center symbol must be a valid character
        sequence[1].isalpha()
    ]

    return TokenType.LIT_CHAR if all(rules) else None

def is_literal_string(sequence: str) -> Optional[TokenType]:

    rules = [

        # Must start and end with double quotes
        sequence[0] == "\"" and sequence[-1] == "\"" 
    ]

    return TokenType.LIT_STRING if all(rules) else None

@dataclass
class Token:
    type: TokenType      = TokenType.NONE,
    line: int            = 0,
    value: Optional[str] = None

class Tokenizer():
    
    def __init__(self, file_path: str = None, contents: str = None):
        
        self.file_path: str                      = file_path
        self.source_file_contents: str           = contents
        
        self.index: int                          = 0
        self.line_number: int                    = 0
        self.tokens: List[Token]                 = []
        
        self.source_file_contents_length:   int  = None
        self.source_file_contents_num_lines: int = None
        
        self.setup()
    
    def __str__(self) -> str:

        intermediate = []

        for token in self.tokens:
            intermediate.append(str(token))

        return ", \n".join(intermediate)
    
    def setup(self):

        if self.file_path is not None:
            
            # Open the source file
            with open(self.file_path) as source_file:
                self.source_file_contents = source_file.read()
            
            # Save the length for future calculations
            self.source_file_contents_length: int = len(self.source_file_contents)

            # Save the total number of lines for future calculations
            self.source_file_contents_num_lines: int = len(self.source_file_contents.splitlines())

        elif self.source_file_contents is not None:
            
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
    
    def parse_space(self) -> str:

        space_buffer = ""
        while self.peek() is not None and self.peek().isspace():
            space_buffer += self.pop()

        return space_buffer

    def parse_char(self) -> str:

        # Consume the first single quote
        char_buffer = self.pop()

        # While we don't see another single quote, build the buffer
        while self.peek() is not None and self.peek() != '\'':
            char_buffer += self.pop()

        # Add the second single quote!
        char_buffer += self.pop()

        return char_buffer
    
    def parse_string(self) -> str:

        # Consume the first single quote
        string_buffer = self.pop()

        # While we don't see another double quote, build the buffer
        while self.peek() is not None and self.peek() != '\"':
            string_buffer += self.pop()

        # If there are more characters, add the second single quote!
        if self.peek() is not None:
            string_buffer += self.pop()

        return string_buffer

    def parse_partial_float(self) -> str:

        """This function parses the 'X' section of a float: AAAAAA.XXXXXXXXf"""

        # Consume the period
        buffer = self.pop()

        while self.peek() is not None and (self.peek().isnumeric() or self.peek() == 'f'):

            # Consume the character
            buffer += self.pop()

            if self.peek() == 'f':

                # Consume the 'f' and break out of this loop
                buffer += self.pop()

        return buffer

    def parse_alphanum(self) -> str:

        buffer = ""

        # While this character is alphanumeric, 
        # build a buffer out of it. If the next character
        # is a period, then we are looking at one of two things:
        # 1) A float literal
        #   - We need to continue consuming the buffer
        #     until an 'f' character is found
        # 2) A field access
        #   - We need to stop!
        #
        # Underscores also need to be accounted for here because they
        # may appear in valid identifiers!
        while self.peek() is not None and (self.peek().isalnum() or self.peek() == '.' or self.peek() == '_'):

            # If the next character is a period...
            if self.peek() == '.':
                
                # ...and the following character is...
                next_two = self.peek(2)

                if next_two is None:
                    print("This shouldn't be possible!")
                    exit(728)
                
                potential_character = next_two[-1]

                # ...alphabetical...
                if potential_character.isalpha():

                    # ... then assume it's a field access and we
                    # need to stop!
                    raise NotImplementedError
                
                # ...numeric...
                elif potential_character.isnumeric():

                    # ...then assume it's a float literal and keep tokenizing it.
                    buffer += self.parse_partial_float()
                    break

            if self.peek() is not None:
                buffer += self.pop()

        return buffer

    def parse_nonalphanum(self) -> str:

        buffer = ""
        peek = self.peek()

        # If this is a single quote
        if peek == "\'":
            buffer = self.parse_char()
        elif peek == "\"":
            buffer = self.parse_string()
        else:
            buffer += self.pop()
        
        return buffer

    def parse_next(self) -> str:

        buffer: str = ""

        # If there is a character to read
        if peek := self.peek():

            # If this character is alphanumeric
            if peek.isalnum():
                buffer = self.parse_alphanum()

            # If this character is not alphanumeric
            else:

                # If this character is a space (or newline!), consume it
                if peek.isspace():
                    buffer = self.parse_space()
                    self.process_newline(buffer)
                else:
                    buffer = self.parse_nonalphanum()

        return buffer

    def process_newline(self, buffer: str) -> None:
        if buffer.find("\n") != -1:
            self.line_number += 1
    
    def tokenize(self) -> Result[None, list[Token]]:
        
        # While there are characters to read
        while self.peek() is not None:

            # Intermediate buffer for building multi-character tokens
            buffer: str = ""
            buffer = self.parse_next()

            # If the buffer is a space or it's empty, then parse space
            if buffer.isspace() or buffer == '':
                pass

            # Is the buffer a character literal?
            elif token_type := is_literal_char(buffer):
                buffer = buffer[1:-1]
                self.tokens.append(Token(token_type, self.line_number, buffer))

            # Is the buffer a string literal?
            elif token_type := is_literal_string(buffer):
                buffer = buffer[1:-1]
                self.tokens.append(Token(token_type, self.line_number, buffer))

            # Is the buffer a valid symbol?
            elif token_type := is_symbol(buffer):
                self.tokens.append(Token(token_type, self.line_number, None))

            # Is the buffer a valid keyword?
            elif token_type := is_keyword(buffer):
                self.tokens.append(Token(token_type, self.line_number, None))

            # Is the buffer a valid identifier?
            elif token_type := is_identifier(buffer):
                self.tokens.append(Token(token_type, self.line_number, buffer))

            # Is the buffer a valid literal?
            elif token_type := is_literal(buffer):
                self.tokens.append(Token(token_type, self.line_number, buffer))

            # Otherwise, ...?
            else:
                return Err("Invalid token!")
        
        # Add an EOF to the end
        self.tokens.append(Token(TokenType.EOF, self.line_number, None))

        return Ok(self.tokens)

