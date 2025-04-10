
import unittest

from Lexer import Token, Tokenizer, TokenType

class TokenizerIntegrationTests(unittest.TestCase):

    def test_minimal_program(self):

        contents = """
        int main(int argc, char** argv) {
            return 0;
        }
        """

        expected_tokens = [
            Token(TokenType.KEYWORD_INT, 1, None),
            Token(TokenType.IDENTIFIER, 1, "main"),
            Token(TokenType.SYM_PAREN_OPEN, 1, None),
            Token(TokenType.KEYWORD_INT, 1, None),
            Token(TokenType.IDENTIFIER, 1, "argc"),
            Token(TokenType.SYM_COMMA, 1, None),
            Token(TokenType.KEYWORD_CHAR, 1, None),
            Token(TokenType.SYM_STAR, 1, None),
            Token(TokenType.SYM_STAR, 1, None),
            Token(TokenType.IDENTIFIER, 1, "argv"),
            Token(TokenType.SYM_PAREN_CLOSE, 1, None),
            Token(TokenType.SYM_BRACE_OPEN, 1, None),
            Token(TokenType.KEYWORD_RETURN, 2, None),
            Token(TokenType.LIT_INT, 2, "0"),
            Token(TokenType.SYM_SEMICOLON, 2, None),
            Token(TokenType.SYM_BRACE_CLOSE, 3, None),
            Token(TokenType.EOF, 4, None),
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_expression_parsing1(self):

        contents = """
        int main(int argc, char** argv) {
            return (a * 29) / (204 - 5) - variable;
        }
        """

        expected_tokens = [
            Token(TokenType.KEYWORD_INT, 1, None),
            Token(TokenType.IDENTIFIER, 1, "main"),
            Token(TokenType.SYM_PAREN_OPEN, 1, None),
            Token(TokenType.KEYWORD_INT, 1, None),
            Token(TokenType.IDENTIFIER, 1, "argc"),
            Token(TokenType.SYM_COMMA, 1, None),
            Token(TokenType.KEYWORD_CHAR, 1, None),
            Token(TokenType.SYM_STAR, 1, None),
            Token(TokenType.SYM_STAR, 1, None),
            Token(TokenType.IDENTIFIER, 1, "argv"),
            Token(TokenType.SYM_PAREN_CLOSE, 1, None),
            Token(TokenType.SYM_BRACE_OPEN, 1, None),
            Token(TokenType.KEYWORD_RETURN, 2, None),
            Token(TokenType.SYM_PAREN_OPEN, 2, None),
            Token(TokenType.IDENTIFIER, 2, "a"),
            Token(TokenType.SYM_STAR, 2, None),
            Token(TokenType.LIT_INT, 2, "29"),
            Token(TokenType.SYM_PAREN_CLOSE, 2, None),
            Token(TokenType.SYM_FSLASH, 2, None),
            Token(TokenType.SYM_PAREN_OPEN, 2, None),
            Token(TokenType.LIT_INT, 2, "204"),
            Token(TokenType.SYM_DASH, 2, None),
            Token(TokenType.LIT_INT, 2, "5"),
            Token(TokenType.SYM_PAREN_CLOSE, 2, None),
            Token(TokenType.SYM_DASH, 2, None),
            Token(TokenType.IDENTIFIER, 2, "variable"),
            Token(TokenType.SYM_SEMICOLON, 2, None),
            Token(TokenType.SYM_BRACE_CLOSE, 3, None),
            Token(TokenType.EOF, 4, None),
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_functions1(self):

        contents = """
        int function2(int a, int b, int c) {
            return a + b + c;
        }
        int f(int a, int b, int c) {
            return a * b + c;
        }
        int main(int argc, char** argv) {
            return f(1, variable1, function2(27, arg2, argv[4]));
        }
        """

        expected_tokens = [
            Token(TokenType.KEYWORD_INT, 1, None),
            Token(TokenType.IDENTIFIER, 1, "function2"),
            Token(TokenType.SYM_PAREN_OPEN, 1, None),
            Token(TokenType.KEYWORD_INT, 1, None),
            Token(TokenType.IDENTIFIER, 1, "a"),
            Token(TokenType.SYM_COMMA, 1, None),
            Token(TokenType.KEYWORD_INT, 1, None),
            Token(TokenType.IDENTIFIER, 1, "b"),
            Token(TokenType.SYM_COMMA, 1, None),
            Token(TokenType.KEYWORD_INT, 1, None),
            Token(TokenType.IDENTIFIER, 1, "c"),
            Token(TokenType.SYM_PAREN_CLOSE, 1, None),
            Token(TokenType.SYM_BRACE_OPEN, 1, None),
            Token(TokenType.KEYWORD_RETURN, 2, None),
            Token(TokenType.IDENTIFIER, 2, "a"),
            Token(TokenType.SYM_PLUS, 2, None),
            Token(TokenType.IDENTIFIER, 2, "b"),
            Token(TokenType.SYM_PLUS, 2, None),
            Token(TokenType.IDENTIFIER, 2, "c"),
            Token(TokenType.SYM_SEMICOLON, 2, None),
            Token(TokenType.SYM_BRACE_CLOSE, 3, None),
            Token(TokenType.KEYWORD_INT, 4, None),
            Token(TokenType.IDENTIFIER, 4, "f"),
            Token(TokenType.SYM_PAREN_OPEN, 4, None),
            Token(TokenType.KEYWORD_INT, 4, None),
            Token(TokenType.IDENTIFIER, 4, "a"),
            Token(TokenType.SYM_COMMA, 4, None),
            Token(TokenType.KEYWORD_INT, 4, None),
            Token(TokenType.IDENTIFIER, 4, "b"),
            Token(TokenType.SYM_COMMA, 4, None),
            Token(TokenType.KEYWORD_INT, 4, None),
            Token(TokenType.IDENTIFIER, 4, "c"),
            Token(TokenType.SYM_PAREN_CLOSE, 4, None),
            Token(TokenType.SYM_BRACE_OPEN, 4, None),
            Token(TokenType.KEYWORD_RETURN, 5, None),
            Token(TokenType.IDENTIFIER, 5, "a"),
            Token(TokenType.SYM_STAR, 5, None),
            Token(TokenType.IDENTIFIER, 5, "b"),
            Token(TokenType.SYM_PLUS, 5, None),
            Token(TokenType.IDENTIFIER, 5, "c"),
            Token(TokenType.SYM_SEMICOLON, 5, None),
            Token(TokenType.SYM_BRACE_CLOSE, 6, None),
            Token(TokenType.KEYWORD_INT, 7, None),
            Token(TokenType.IDENTIFIER, 7, "main"),
            Token(TokenType.SYM_PAREN_OPEN, 7, None),
            Token(TokenType.KEYWORD_INT, 7, None),
            Token(TokenType.IDENTIFIER, 7, "argc"),
            Token(TokenType.SYM_COMMA, 7, None),
            Token(TokenType.KEYWORD_CHAR, 7, None),
            Token(TokenType.SYM_STAR, 7, None),
            Token(TokenType.SYM_STAR, 7, None),
            Token(TokenType.IDENTIFIER, 7, "argv"),
            Token(TokenType.SYM_PAREN_CLOSE, 7, None),
            Token(TokenType.SYM_BRACE_OPEN, 7, None),
            Token(TokenType.KEYWORD_RETURN, 8, None),
            Token(TokenType.IDENTIFIER, 8, "f"),
            Token(TokenType.SYM_PAREN_OPEN, 8, None),
            Token(TokenType.LIT_INT, 8, "1"),
            Token(TokenType.SYM_COMMA, 8, None),
            Token(TokenType.IDENTIFIER, 8, "variable1"),
            Token(TokenType.SYM_COMMA, 8, None),
            Token(TokenType.IDENTIFIER, 8, "function2"),
            Token(TokenType.SYM_PAREN_OPEN, 8, None),
            Token(TokenType.LIT_INT, 8, "27"),
            Token(TokenType.SYM_COMMA, 8, None),
            Token(TokenType.IDENTIFIER, 8, "arg2"),
            Token(TokenType.SYM_COMMA, 8, None),
            Token(TokenType.IDENTIFIER, 8, "argv"),
            Token(TokenType.SYM_BRACKET_OPEN, 8, None),
            Token(TokenType.LIT_INT, 8, "4"),
            Token(TokenType.SYM_BRACKET_CLOSE, 8, None),
            Token(TokenType.SYM_PAREN_CLOSE, 8, None),
            Token(TokenType.SYM_PAREN_CLOSE, 8, None),
            Token(TokenType.SYM_SEMICOLON, 8, None),
            Token(TokenType.SYM_BRACE_CLOSE, 9, None),
            Token(TokenType.EOF, 10, None),
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_structs(self):

        contents = """
        struct point {
            int x;
            int y;
        }; 
        """

        expected_tokens = [
            Token(TokenType.KEYWORD_STRUCT, 1, None),
            Token(TokenType.IDENTIFIER, 1, "point"),
            Token(TokenType.SYM_BRACE_OPEN, 1, None),
            Token(TokenType.KEYWORD_INT, 2, None),
            Token(TokenType.IDENTIFIER, 2, "x"),
            Token(TokenType.SYM_SEMICOLON, 2, None),
            Token(TokenType.KEYWORD_INT, 3, None),
            Token(TokenType.IDENTIFIER, 3, "y"),
            Token(TokenType.SYM_SEMICOLON, 3, None),
            Token(TokenType.SYM_BRACE_CLOSE, 4, None),
            Token(TokenType.SYM_SEMICOLON, 4, None),
            Token(TokenType.EOF, 5, None),
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_typedefs(self):

        contents = """
        struct point {
            int x;
            int y;
        }; 
        """

        expected_tokens = [
            Token(TokenType.KEYWORD_STRUCT, 1, None),
            Token(TokenType.IDENTIFIER, 1, "point"),
            Token(TokenType.SYM_BRACE_OPEN, 1, None),
            Token(TokenType.KEYWORD_INT, 2, None),
            Token(TokenType.IDENTIFIER, 2, "x"),
            Token(TokenType.SYM_SEMICOLON, 2, None),
            Token(TokenType.KEYWORD_INT, 3, None),
            Token(TokenType.IDENTIFIER, 3, "y"),
            Token(TokenType.SYM_SEMICOLON, 3, None),
            Token(TokenType.SYM_BRACE_CLOSE, 4, None),
            Token(TokenType.SYM_SEMICOLON, 4, None),
            Token(TokenType.EOF, 5, None),
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

class TokenizerUnitTestsForSymbols(unittest.TestCase):
    
    def test_symbol_semicolon(self):
        
        contents = """;"""

        expected_tokens = [
            Token(TokenType.SYM_SEMICOLON, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_colon(self):
        
        contents = """:"""

        expected_tokens = [
            Token(TokenType.SYM_COLON, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_comma(self):
        
        contents = ""","""

        expected_tokens = [
            Token(TokenType.SYM_COMMA, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_question(self):
        
        contents = """?"""

        expected_tokens = [
            Token(TokenType.SYM_QUESTION, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_paren_open(self):
        
        contents = """("""

        expected_tokens = [
            Token(TokenType.SYM_PAREN_OPEN, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_paren_close(self):
        
        contents = """)"""

        expected_tokens = [
            Token(TokenType.SYM_PAREN_CLOSE, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_brace_open(self):
        
        contents = """{"""

        expected_tokens = [
            Token(TokenType.SYM_BRACE_OPEN, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_brace_close(self):
        
        contents = """}"""

        expected_tokens = [
            Token(TokenType.SYM_BRACE_CLOSE, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_bracket_open(self):
        
        contents = """["""

        expected_tokens = [
            Token(TokenType.SYM_BRACKET_OPEN, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_bracket_close(self):
        
        contents = """]"""

        expected_tokens = [
            Token(TokenType.SYM_BRACKET_CLOSE, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_equal(self):
        
        contents = """="""

        expected_tokens = [
            Token(TokenType.SYM_EQUAL, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_plus(self):
        
        contents = """+"""

        expected_tokens = [
            Token(TokenType.SYM_PLUS, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_minus(self):
        
        contents = """-"""

        expected_tokens = [
            Token(TokenType.SYM_DASH, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_fslash(self):
        
        contents = """/"""

        expected_tokens = [
            Token(TokenType.SYM_FSLASH, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_star(self):
        
        contents = """*"""

        expected_tokens = [
            Token(TokenType.SYM_STAR, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_percent(self):
        
        contents = """%"""

        expected_tokens = [
            Token(TokenType.SYM_PERCENT, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_exclaim(self):
        
        contents = """!"""

        expected_tokens = [
            Token(TokenType.SYM_EXCLAIM, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_less_than(self):
        
        contents = """<"""

        expected_tokens = [
            Token(TokenType.SYM_LT, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_greater_than(self):
        
        contents = """>"""

        expected_tokens = [
            Token(TokenType.SYM_GT, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_ampersand(self):
        
        contents = """&"""

        expected_tokens = [
            Token(TokenType.SYM_AMPERSAND, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_pipe(self):
        
        contents = """|"""

        expected_tokens = [
            Token(TokenType.SYM_PIPE, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
        
    def test_symbol_caret(self):
        
        contents = """^"""

        expected_tokens = [
            Token(TokenType.SYM_CARET, 0, None),
            Token(TokenType.EOF, 0, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
    
    @unittest.skip("A lone single quote cannot appear in a valid Aries program. This test is designed to find just one instance of a symbol, but this is not valid for single quotes. Unsure what to do. Should it look for two quotes? Should a lone single quote generate a more useful error? Should empty character literals be supported?")
    def test_symbol_squote(self):
        
        contents = """\'"""

        expected_tokens = [
            Token(TokenType.SYM_SQUOTE, None, None),
            Token(TokenType.SYM_SQUOTE, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
    
    @unittest.skip("A lone double quote cannot appear in a valid Aries program. This test is designed to find just one instance of a symbol, but this is not valid for double quotes. Unsure what to do. Should it look for two quotes? Should a lone double quote generate a more useful error? Should empty character literals be supported?")
    def test_symbol_dquote(self):
        
        contents = """\""""

        expected_tokens = [
            Token(TokenType.SYM_DQUOTE, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
    
class TokenizerUnitTestsForKeywords(unittest.TestCase):

    def test_all_keywords(self):

        # A list of all supported C keywords
        all_keywords = [
            "bool",
            "break",
            "case",
            "char",
            "const",
            "continue",
            "default",
            "else",
            "enum",
            "float",
            "for",
            "if",
            "int",
            "nullptr",
            "return",
            "sizeof",
            "static",
            "struct",
            "switch",
            "typedef",
            "unsigned",
            "void",
            "while",
        ]

        all_keywords_token_types = [
            TokenType.KEYWORD_BOOL,
            TokenType.KEYWORD_BREAK,
            TokenType.KEYWORD_CASE,
            TokenType.KEYWORD_CHAR,
            TokenType.KEYWORD_CONST,
            TokenType.KEYWORD_CONTINUE,
            TokenType.KEYWORD_DEFAULT,
            TokenType.KEYWORD_ELSE,
            TokenType.KEYWORD_ENUM,
            TokenType.KEYWORD_FLOAT,
            TokenType.KEYWORD_FOR,
            TokenType.KEYWORD_IF,
            TokenType.KEYWORD_INT,
            TokenType.KEYWORD_NULLPTR,
            TokenType.KEYWORD_RETURN,
            TokenType.KEYWORD_SIZEOF,
            TokenType.KEYWORD_STATIC,
            TokenType.KEYWORD_STRUCT,
            TokenType.KEYWORD_SWITCH,
            TokenType.KEYWORD_TYPEDEF,
            TokenType.KEYWORD_UNSIGNED,
            TokenType.KEYWORD_VOID,
            TokenType.KEYWORD_WHILE,
        ]

        for (index, keyword) in enumerate(all_keywords):

            expected_tokens = [
                Token(all_keywords_token_types[index], 0, None),
                Token(TokenType.EOF, 0, None)
            ]

            tokenizer = Tokenizer(contents=keyword)
            actual_tokens_r = tokenizer.tokenize()
            if actual_tokens_r.is_err:
                self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
            
            actual_tokens = actual_tokens_r.unwrap()

            self.assertListEqual(expected_tokens, actual_tokens)

class TokenizerUnitTestsForLiterals(unittest.TestCase):
    
    def test_literal_unsigned_integer1(self):
        
        actual_file_contents = """255u"""
        
        tokenizer = Tokenizer(contents=actual_file_contents)
        actual_token_list_r = tokenizer.tokenize()
        if actual_token_list_r.is_err:
            self.fail(f"Failed to tokenize: {actual_token_list_r.unwrap_err()}")
        actual_token_list = actual_token_list_r.unwrap()
        
        expected_token_list = [
            Token(TokenType.LIT_UINT, 0, "255u"),
            Token(TokenType.EOF, 0, None),
        ]
        
        self.assertListEqual(actual_token_list, expected_token_list)
    
    def test_literal_integer1(self):
        
        actual_file_contents = """12378"""
        
        tokenizer = Tokenizer(contents=actual_file_contents)
        actual_token_list_r = tokenizer.tokenize()
        if actual_token_list_r.is_err:
            self.fail(f"Failed to tokenize: {actual_token_list_r.unwrap_err()}")
        actual_token_list = actual_token_list_r.unwrap()
        
        expected_token_list = [
            Token(TokenType.LIT_INT, 0, "12378"),
            Token(TokenType.EOF, 0, None),
        ]
        
        self.assertListEqual(actual_token_list, expected_token_list)
        
    def test_literal_integer2(self):
        
        actual_file_contents = """-2378"""
        
        tokenizer = Tokenizer(contents=actual_file_contents)
        actual_token_list_r = tokenizer.tokenize()
        if actual_token_list_r.is_err:
            self.fail(f"Failed to tokenize: {actual_token_list_r.unwrap_err()}")
        actual_token_list = actual_token_list_r.unwrap()
        
        expected_token_list = [
            Token(TokenType.SYM_DASH, 0, None),
            Token(TokenType.LIT_INT, 0, "2378"),
            Token(TokenType.EOF, 0, None),
        ]
        
        self.assertListEqual(actual_token_list, expected_token_list)

    def test_literal_string1(self):
        
        actual_file_contents = """\"test string @ $#**()}!\""""
        
        tokenizer = Tokenizer(contents=actual_file_contents)
        actual_token_list_r = tokenizer.tokenize()
        if actual_token_list_r.is_err:
            self.fail(f"Failed to tokenize: {actual_token_list_r.unwrap_err()}")
        actual_token_list = actual_token_list_r.unwrap()
        
        expected_token_list = [
            Token(TokenType.LIT_STRING, 0, "test string @ $#**()}!"),
            Token(TokenType.EOF, 0, None),
        ]
        
        self.assertListEqual(actual_token_list, expected_token_list)
    
    def test_literal_string_empty(self):
        
        actual_file_contents = """\"\""""
        
        tokenizer = Tokenizer(contents=actual_file_contents)
        actual_token_list_r = tokenizer.tokenize()
        if actual_token_list_r.is_err:
            self.fail(f"Failed to tokenize: {actual_token_list_r.unwrap_err()}")
        actual_token_list = actual_token_list_r.unwrap()
        
        expected_token_list = [
            Token(TokenType.LIT_STRING, 0, ""),
            Token(TokenType.EOF, 0, None),
        ]
        
        self.assertListEqual(actual_token_list, expected_token_list)

    def test_literal_string_no_end_quote(self):
        
        actual_file_contents = """\"test"""
        
        tokenizer = Tokenizer(contents=actual_file_contents)
        actual_token_list_r = tokenizer.tokenize()
        self.assertTrue(actual_token_list_r.is_err)

    def test_literal_character1(self):
        
        actual_file_contents = """'s'"""
        
        tokenizer = Tokenizer(contents=actual_file_contents)
        actual_token_list_r = tokenizer.tokenize()
        if actual_token_list_r.is_err:
            self.fail(f"Failed to tokenize: {actual_token_list_r.unwrap_err()}")
        actual_token_list = actual_token_list_r.unwrap()
        
        expected_token_list = [
            Token(TokenType.LIT_CHAR, 0, "s"),
            Token(TokenType.EOF, 0, None),
        ]
        
        self.assertListEqual(actual_token_list, expected_token_list)
    
    def test_literal_character_empty(self):
        
        actual_file_contents = """''"""
        
        tokenizer = Tokenizer(contents=actual_file_contents)
        actual_token_list_r = tokenizer.tokenize()
        if actual_token_list_r.is_err:
            self.fail(f"Failed to tokenize: {actual_token_list_r.unwrap_err()}")
        actual_token_list = actual_token_list_r.unwrap()
        
        expected_token_list = [
            Token(TokenType.LIT_CHAR, 0, ""),
            Token(TokenType.EOF, 0, None),
        ]
        
        self.assertListEqual(actual_token_list, expected_token_list)

    def test_literal_character_invalid(self):
        
        actual_file_contents = """'too long!'"""
        
        tokenizer = Tokenizer(contents=actual_file_contents)
        actual_token_list_r = tokenizer.tokenize()
        self.assertTrue(actual_token_list_r.is_err)
    
    def test_literal_float1(self):
        
        actual_file_contents = """3.14159265f"""
        
        tokenizer = Tokenizer(contents=actual_file_contents)
        actual_token_list_r = tokenizer.tokenize()
        if actual_token_list_r.is_err:
            self.fail(f"Failed to tokenize: {actual_token_list_r.unwrap_err()}")
        actual_token_list = actual_token_list_r.unwrap()
        
        expected_token_list = [
            Token(TokenType.LIT_FLOAT, 0, "3.14159265f"),
            Token(TokenType.EOF, 0, None),
        ]
        
        self.assertListEqual(actual_token_list, expected_token_list)

    def test_literal_float2(self):
        
        actual_file_contents = """1.0f"""
        
        tokenizer = Tokenizer(contents=actual_file_contents)
        actual_token_list_r = tokenizer.tokenize()
        if actual_token_list_r.is_err:
            self.fail(f"Failed to tokenize: {actual_token_list_r.unwrap_err()}")
        actual_token_list = actual_token_list_r.unwrap()
        
        expected_token_list = [
            Token(TokenType.LIT_FLOAT, 0, "1.0f"),
            Token(TokenType.EOF, 0, None),
        ]
        
        self.assertListEqual(actual_token_list, expected_token_list)

    def test_literal_float3(self):
        
        actual_file_contents = """-278f"""
        
        tokenizer = Tokenizer(contents=actual_file_contents)
        actual_token_list_r = tokenizer.tokenize()
        if actual_token_list_r.is_err:
            self.fail(f"Failed to tokenize: {actual_token_list_r.unwrap_err()}")
        actual_token_list = actual_token_list_r.unwrap()
        
        expected_token_list = [
            Token(TokenType.SYM_DASH, 0, None),
            Token(TokenType.LIT_FLOAT, 0, "278f"),
            Token(TokenType.EOF, 0, None),
        ]
        
        self.assertListEqual(actual_token_list, expected_token_list)
