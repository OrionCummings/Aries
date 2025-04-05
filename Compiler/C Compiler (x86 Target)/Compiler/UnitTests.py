
import unittest

from Lexer import Token, Tokenizer, TokenType


class TokenizerUnitTests(unittest.TestCase):
    
    test_dir = "D:\\PersonalProjects\\Aries\\Compiler\\C Compiler (x86 Target)\\Test Files\\"
    
    def test_return_literal_unsigned_integer(self):
        
        actual_file_contents = """
        uint f() {
            return 255u;
        }
        """
        
        tokenizer = Tokenizer(contents=actual_file_contents)
        actual_token_list_r = tokenizer.tokenize()
        if actual_token_list_r.is_err:
            self.fail(f"Failed to tokenize: {actual_token_list_r.unwrap_err()}")
        actual_token_list = actual_token_list_r.unwrap()
        
        expected_token_list = [
            Token(TokenType.KEYWORD_UINT, None, None),
            Token(TokenType.IDENTIFIER, None, "f"),
            Token(TokenType.SYM_PAREN_OPEN, None, None),
            Token(TokenType.SYM_PAREN_CLOSE, None, None),
            Token(TokenType.SYM_BRACE_OPEN, None, None),
            Token(TokenType.KEYWORD_RETURN, None, None),
            Token(TokenType.LIT_UINT, None, "255u"),
            Token(TokenType.SYM_SEMICOLON, None, None),
            Token(TokenType.SYM_BRACE_CLOSE, None, None),
            Token(TokenType.EOF, None, None),
        ]
        
        self.assertListEqual(actual_token_list, expected_token_list)
    
    def test_return_literal_integer(self):
        
        actual_file_contents = """
        int f() {
            return 0;
        }
        """
        
        tokenizer = Tokenizer(contents=actual_file_contents)
        actual_token_list_r = tokenizer.tokenize()
        if actual_token_list_r.is_err:
            self.fail(f"Failed to tokenize: {actual_token_list_r.unwrap_err()}")
        actual_token_list = actual_token_list_r.unwrap()
        
        expected_token_list = [
            Token(TokenType.KEYWORD_INT, None, None),
            Token(TokenType.IDENTIFIER, None, "f"),
            Token(TokenType.SYM_PAREN_OPEN, None, None),
            Token(TokenType.SYM_PAREN_CLOSE, None, None),
            Token(TokenType.SYM_BRACE_OPEN, None, None),
            Token(TokenType.KEYWORD_RETURN, None, None),
            Token(TokenType.LIT_INT, None, "0"),
            Token(TokenType.SYM_SEMICOLON, None, None),
            Token(TokenType.SYM_BRACE_CLOSE, None, None),
            Token(TokenType.EOF, None, None),
        ]
        
        self.assertListEqual(actual_token_list, expected_token_list)
        
    def test_return_literal_string(self):
        
        actual_file_contents = """
        char* f() {
            return "test string @ $#**()}!";
        }
        """
        
        tokenizer = Tokenizer(contents=actual_file_contents)
        actual_token_list_r = tokenizer.tokenize()
        if actual_token_list_r.is_err:
            self.fail(f"Failed to tokenize: {actual_token_list_r.unwrap_err()}")
        actual_token_list = actual_token_list_r.unwrap()
        
        expected_token_list = [
            Token(TokenType.KEYWORD_CHAR, None, None),
            Token(TokenType.SYM_STAR, None, None),
            Token(TokenType.IDENTIFIER, None, "f"),
            Token(TokenType.SYM_PAREN_OPEN, None, None),
            Token(TokenType.SYM_PAREN_CLOSE, None, None),
            Token(TokenType.SYM_BRACE_OPEN, None, None),
            Token(TokenType.KEYWORD_RETURN, None, None),
            Token(TokenType.LIT_STRING, None, "test string @ $#**()}!"),
            Token(TokenType.SYM_SEMICOLON, None, None),
            Token(TokenType.SYM_BRACE_CLOSE, None, None),
            Token(TokenType.EOF, None, None),
        ]
        
        self.assertListEqual(actual_token_list, expected_token_list)
        
    def test_return_literal_character(self):
        
        actual_file_contents = """
        char f() {
            return 's';
        }
        """
        
        tokenizer = Tokenizer(contents=actual_file_contents)
        actual_token_list_r = tokenizer.tokenize()
        if actual_token_list_r.is_err:
            self.fail(f"Failed to tokenize: {actual_token_list_r.unwrap_err()}")
        actual_token_list = actual_token_list_r.unwrap()
        
        expected_token_list = [
            Token(TokenType.KEYWORD_CHAR, None, None),
            Token(TokenType.IDENTIFIER, None, "f"),
            Token(TokenType.SYM_PAREN_OPEN, None, None),
            Token(TokenType.SYM_PAREN_CLOSE, None, None),
            Token(TokenType.SYM_BRACE_OPEN, None, None),
            Token(TokenType.KEYWORD_RETURN, None, None),
            Token(TokenType.LIT_CHAR, None, "s"),
            Token(TokenType.SYM_SEMICOLON, None, None),
            Token(TokenType.SYM_BRACE_CLOSE, None, None),
            Token(TokenType.EOF, None, None),
        ]
        
        self.assertListEqual(actual_token_list, expected_token_list)
        
    def test_return_literal_float(self):
        
        actual_file_contents = """
        3.14159265f
        """
        
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

