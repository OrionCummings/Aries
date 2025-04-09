
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
            Token(TokenType.LIT_INT, None, "0"),
            Token(TokenType.SYM_SEMICOLON, None, None),
            Token(TokenType.SYM_BRACE_CLOSE, None, None),
            Token(TokenType.EOF, None, None),
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
            Token(TokenType.SYM_PAREN_OPEN, None, None),
            Token(TokenType.IDENTIFIER, None, "a"),
            Token(TokenType.SYM_STAR, None, None),
            Token(TokenType.LIT_INT, None, "29"),
            Token(TokenType.SYM_PAREN_CLOSE, None, None),
            Token(TokenType.SYM_FSLASH, None, None),
            Token(TokenType.SYM_PAREN_OPEN, None, None),
            Token(TokenType.LIT_INT, None, "204"),
            Token(TokenType.SYM_DASH, None, None),
            Token(TokenType.LIT_INT, None, "5"),
            Token(TokenType.SYM_PAREN_CLOSE, None, None),
            Token(TokenType.SYM_DASH, None, None),
            Token(TokenType.IDENTIFIER, None, "variable"),
            Token(TokenType.SYM_SEMICOLON, None, None),
            Token(TokenType.SYM_BRACE_CLOSE, None, None),
            Token(TokenType.EOF, None, None),
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
            Token(TokenType.KEYWORD_INT, None, None),
            Token(TokenType.IDENTIFIER, None, "function2"),
            Token(TokenType.SYM_PAREN_OPEN, None, None),
            Token(TokenType.KEYWORD_INT, None, None),
            Token(TokenType.IDENTIFIER, None, "a"),
            Token(TokenType.SYM_COMMA, None, None),
            Token(TokenType.KEYWORD_INT, None, None),
            Token(TokenType.IDENTIFIER, None, "b"),
            Token(TokenType.SYM_COMMA, None, None),
            Token(TokenType.KEYWORD_INT, None, None),
            Token(TokenType.IDENTIFIER, None, "c"),
            Token(TokenType.SYM_PAREN_CLOSE, None, None),
            Token(TokenType.SYM_BRACE_OPEN, None, None),
            Token(TokenType.KEYWORD_RETURN, None, None),
            Token(TokenType.IDENTIFIER, None, "a"),
            Token(TokenType.SYM_PLUS, None, None),
            Token(TokenType.IDENTIFIER, None, "b"),
            Token(TokenType.SYM_PLUS, None, None),
            Token(TokenType.IDENTIFIER, None, "c"),
            Token(TokenType.SYM_SEMICOLON, None, None),
            Token(TokenType.SYM_BRACE_CLOSE, None, None),
            Token(TokenType.KEYWORD_INT, None, None),
            Token(TokenType.IDENTIFIER, None, "f"),
            Token(TokenType.SYM_PAREN_OPEN, None, None),
            Token(TokenType.KEYWORD_INT, None, None),
            Token(TokenType.IDENTIFIER, None, "a"),
            Token(TokenType.SYM_COMMA, None, None),
            Token(TokenType.KEYWORD_INT, None, None),
            Token(TokenType.IDENTIFIER, None, "b"),
            Token(TokenType.SYM_COMMA, None, None),
            Token(TokenType.KEYWORD_INT, None, None),
            Token(TokenType.IDENTIFIER, None, "c"),
            Token(TokenType.SYM_PAREN_CLOSE, None, None),
            Token(TokenType.SYM_BRACE_OPEN, None, None),
            Token(TokenType.KEYWORD_RETURN, None, None),
            Token(TokenType.IDENTIFIER, None, "a"),
            Token(TokenType.SYM_STAR, None, None),
            Token(TokenType.IDENTIFIER, None, "b"),
            Token(TokenType.SYM_PLUS, None, None),
            Token(TokenType.IDENTIFIER, None, "c"),
            Token(TokenType.SYM_SEMICOLON, None, None),
            Token(TokenType.SYM_BRACE_CLOSE, None, None),
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
            Token(TokenType.IDENTIFIER, None, "f"),
            Token(TokenType.SYM_PAREN_OPEN, None, None),
            Token(TokenType.LIT_INT, None, "1"),
            Token(TokenType.SYM_COMMA, None, None),
            Token(TokenType.IDENTIFIER, None, "variable1"),
            Token(TokenType.SYM_COMMA, None, None),
            Token(TokenType.IDENTIFIER, None, "function2"),
            Token(TokenType.SYM_PAREN_OPEN, None, None),
            Token(TokenType.LIT_INT, None, "27"),
            Token(TokenType.SYM_COMMA, None, None),
            Token(TokenType.IDENTIFIER, None, "arg2"),
            Token(TokenType.SYM_COMMA, None, None),
            Token(TokenType.IDENTIFIER, None, "argv"),
            Token(TokenType.SYM_BRACKET_OPEN, None, None),
            Token(TokenType.LIT_INT, None, "4"),
            Token(TokenType.SYM_BRACKET_CLOSE, None, None),
            Token(TokenType.SYM_PAREN_CLOSE, None, None),
            Token(TokenType.SYM_PAREN_CLOSE, None, None),
            Token(TokenType.SYM_SEMICOLON, None, None),
            Token(TokenType.SYM_BRACE_CLOSE, None, None),
            Token(TokenType.EOF, None, None),
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
            Token(TokenType.SYM_SEMICOLON, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_COLON, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_COMMA, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_QUESTION, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_PAREN_OPEN, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_PAREN_CLOSE, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_BRACE_OPEN, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_BRACE_CLOSE, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_BRACKET_OPEN, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_BRACKET_CLOSE, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_EQUAL, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_PLUS, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_DASH, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_FSLASH, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_STAR, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_PERCENT, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_EXCLAIM, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_LT, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_GT, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_AMPERSAND, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_PIPE, None, None),
            Token(TokenType.EOF, None, None)
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
            Token(TokenType.SYM_CARET, None, None),
            Token(TokenType.EOF, None, None)
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
    
    def test_keyword_if(self):

        contents = """if"""

        expected_tokens = [
            Token(TokenType.KEYWORD_IF, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
    
    def test_keyword_while(self):

        contents = """while"""

        expected_tokens = [
            Token(TokenType.KEYWORD_WHILE, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_for(self):

        contents = """for"""

        expected_tokens = [
            Token(TokenType.KEYWORD_FOR, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
    
    def test_keyword_continue(self):

        contents = """continue"""

        expected_tokens = [
            Token(TokenType.KEYWORD_CONTINUE, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
    
    def test_keyword_match(self):

        contents = """match"""

        expected_tokens = [
            Token(TokenType.KEYWORD_MATCH, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
    
    def test_keyword_switch(self):

        contents = """switch"""

        expected_tokens = [
            Token(TokenType.KEYWORD_SWITCH, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
    
    def test_keyword_case(self):

        contents = """case"""

        expected_tokens = [
            Token(TokenType.KEYWORD_CASE, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
    
    def test_keyword_break(self):

        contents = """break"""

        expected_tokens = [
            Token(TokenType.KEYWORD_BREAK, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
    
    def test_keyword_default(self):

        contents = """default"""

        expected_tokens = [
            Token(TokenType.KEYWORD_DEFAULT, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)
    
    def test_keyword_def(self):

        contents = """def"""

        expected_tokens = [
            Token(TokenType.KEYWORD_DEF, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_struct(self):

        contents = """struct"""

        expected_tokens = [
            Token(TokenType.KEYWORD_STRUCT, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_enum(self):

        contents = """enum"""

        expected_tokens = [
            Token(TokenType.KEYWORD_ENUM, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_overload(self):

        contents = """overload"""

        expected_tokens = [
            Token(TokenType.KEYWORD_OVERLOAD, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_const(self):

        contents = """const"""

        expected_tokens = [
            Token(TokenType.KEYWORD_CONST, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_static(self):

        contents = """static"""

        expected_tokens = [
            Token(TokenType.KEYWORD_STATIC, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_mut(self):

        contents = """mut"""

        expected_tokens = [
            Token(TokenType.KEYWORD_MUTABLE, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_return(self):

        contents = """return"""

        expected_tokens = [
            Token(TokenType.KEYWORD_RETURN, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_sizeof(self):

        contents = """sizeof"""

        expected_tokens = [
            Token(TokenType.KEYWORD_SIZEOF, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_typeof(self):

        contents = """typeof"""

        expected_tokens = [
            Token(TokenType.KEYWORD_TYPEOF, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_as(self):

        contents = """as"""

        expected_tokens = [
            Token(TokenType.KEYWORD_CAST, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_asm(self):

        contents = """asm"""

        expected_tokens = [
            Token(TokenType.KEYWORD_ASM, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_new(self):

        contents = """new"""

        expected_tokens = [
            Token(TokenType.KEYWORD_NEW, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_true(self):

        contents = """true"""

        expected_tokens = [
            Token(TokenType.KEYWORD_TRUE, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_false(self):

        contents = """false"""

        expected_tokens = [
            Token(TokenType.KEYWORD_FALSE, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_bool(self):

        contents = """bool"""

        expected_tokens = [
            Token(TokenType.KEYWORD_BOOL, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_int(self):

        contents = """int"""

        expected_tokens = [
            Token(TokenType.KEYWORD_INT, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_uint(self):

        contents = """uint"""

        expected_tokens = [
            Token(TokenType.KEYWORD_UINT, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_float(self):

        contents = """float"""

        expected_tokens = [
            Token(TokenType.KEYWORD_FLOAT, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_char(self):

        contents = """char"""

        expected_tokens = [
            Token(TokenType.KEYWORD_CHAR, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_string(self):

        contents = """string"""

        expected_tokens = [
            Token(TokenType.KEYWORD_STRING, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
        actual_tokens_r = tokenizer.tokenize()
        if actual_tokens_r.is_err:
            self.fail(f"Failed to tokenize: {actual_tokens_r.unwrap_err()}")
        
        actual_tokens = actual_tokens_r.unwrap()

        self.assertListEqual(expected_tokens, actual_tokens)

    def test_keyword_void(self):

        contents = """void"""

        expected_tokens = [
            Token(TokenType.KEYWORD_VOID, None, None),
            Token(TokenType.EOF, None, None)
        ]

        tokenizer = Tokenizer(contents=contents)
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
            Token(TokenType.LIT_UINT, None, "255u"),
            Token(TokenType.EOF, None, None),
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
            Token(TokenType.LIT_INT, None, "12378"),
            Token(TokenType.EOF, None, None),
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
            Token(TokenType.SYM_DASH, None, None),
            Token(TokenType.LIT_INT, None, "2378"),
            Token(TokenType.EOF, None, None),
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
            Token(TokenType.LIT_STRING, None, "test string @ $#**()}!"),
            Token(TokenType.EOF, None, None),
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
            Token(TokenType.LIT_STRING, None, ""),
            Token(TokenType.EOF, None, None),
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
            Token(TokenType.LIT_CHAR, None, "s"),
            Token(TokenType.EOF, None, None),
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
            Token(TokenType.LIT_FLOAT, None, "3.14159265f"),
            Token(TokenType.EOF, None, None),
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
            Token(TokenType.LIT_FLOAT, None, "1.0f"),
            Token(TokenType.EOF, None, None),
        ]
        
        self.assertListEqual(actual_token_list, expected_token_list)

    def test_literal_float3(self):
        
        actual_file_contents = """278f"""
        
        tokenizer = Tokenizer(contents=actual_file_contents)
        actual_token_list_r = tokenizer.tokenize()
        if actual_token_list_r.is_err:
            self.fail(f"Failed to tokenize: {actual_token_list_r.unwrap_err()}")
        actual_token_list = actual_token_list_r.unwrap()
        
        expected_token_list = [
            Token(TokenType.LIT_FLOAT, None, "278f"),
            Token(TokenType.EOF, None, None),
        ]
        
        self.assertListEqual(actual_token_list, expected_token_list)
