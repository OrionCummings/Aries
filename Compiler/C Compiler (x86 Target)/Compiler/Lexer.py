from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, List, Optional
from option import Err, Ok, Result

class TokenType(Enum):
    NONE                    = auto(),
    EXIT                    = auto(),
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
    SYM_CARRET              = auto(), # ^
    SYM_SQUOTE              = auto(), # '
    SYM_DQUOTE              = auto(), # "
    LIT_INT                 = auto(), # integers
    LIT_UINT                = auto(), # unsigned integers
    LIT_FLOAT               = auto(), # floats
    LIT_CHAR                = auto(), # characters
    LIT_STRING              = auto(), # strings
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
    KEYWORD_MUTABLE         = auto(), # mutable
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
    KEYWORD_BOOL            = auto(), # boolean
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
    "mut":          TokenType.KEYWORD_MUTABLE,
    "return":       TokenType.KEYWORD_RETURN,
    "sizeof":       TokenType.KEYWORD_SIZEOF,
    "typeof":       TokenType.KEYWORD_TYPEOF,
    "as":           TokenType.KEYWORD_CAST,
    "asm":          TokenType.KEYWORD_ASM,
    "new":          TokenType.KEYWORD_NEW,
    "true":         TokenType.KEYWORD_TRUE,
    "false":        TokenType.KEYWORD_FALSE,
    "bool":         TokenType.KEYWORD_BOOL,
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
    
    return TokenType.LIT_UINT if any(rules) else None

def is_literal_float(sequence: str) -> Optional[TokenType]:

    rules = [

        # Must end with 'f'
        sequence[-1] == 'f', 

        # If one f and one period are replaced, the number must be numeric
        sequence.replace('f', '', count=1).replace('.', '', count=1).isnumeric()
    ]
    
    return TokenType.LIT_FLOAT if any(rules) else None

def is_literal_char(sequence: str) -> Optional[TokenType]:

    # If any of these conditions are true, then this cannot be
    # a character literal. Furthermore, the more general 'rules'
    # will fail if these disqualifying rules are not checked first!
    disqualifying_rules = [
        len(sequence) < 3,
    ]

    if any(disqualifying_rules):
        return None

    rules = [

        # Must be three characters total (' x ')
        len(sequence) == 3,

        # Must start and end with single quotes
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

    return TokenType.LITERAL if all(rules) else None
    
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
        self.line_count: int                     = 1
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
    
    def parse_next(self) -> str:

        buffer: str = ""

        # If there is a character to read
        if peek := self.peek():

            # If this character is a space (or newline!), consume it
            if peek.isspace():
                self.pop()

            # If this character is alphanumeric
            elif peek.isalnum():

                # While this character is alphanumeric, 
                # build a buffer out of it. If the next character
                # is a period, then we are looking at one of two things:
                # 1) A float literal
                #   - We need to continue consuming the buffer
                #     until an 'f' character is found
                # 2) A field access
                #   - We need to stop!
                while self.peek().isalnum() or self.peek() == '.':

                    # If the next character is a period...
                    if self.peek() == '.':
                        
                        # ...and the following character is...
                        # TODO: This will fail on suffciently incorrect inputs!
                        next_two = self.peek(2)
                        potential_character = next_two[-1]

                        # ...alphabetical...
                        if potential_character.isalpha():

                            # ... then assume it's a field access and we
                            # need to stop!
                            raise NotImplementedError
                        
                        # ...numeric...
                        elif potential_character.isnumeric():

                            # ...then assume it's a float literal and
                            # keep tokenizing it.

                            # Consume the period
                            buffer += self.pop()

                            while self.peek().isnumeric() or self.peek() == 'f':

                                if self.peek() == 'f':

                                    # Consume the 'f' and continue
                                    buffer += self.pop()

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
    
    def tokenize(self) -> Result[None, list[Token]]:
        
        # Intermediate buffer for building multi-character tokens
        buffer: str = ""
        
        # While there are characters to read
        while self.peek() is not None:

            buffer = self.parse_next()
            pass

            # DEBUG:
            if not buffer == '':
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
                    self.tokens.append(Token(TokenType.LIT_CHAR, None, buffer))

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
                self.tokens.append(Token(TokenType.LIT_STRING, None, buffer))

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

