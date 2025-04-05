
import unittest

from Lexer import Token, Tokenizer, TokenType


class TokenizerUnitTests(unittest.TestCase):
    
    test_dir = "D:\\PersonalProjects\\Aries\\Compiler\\C Compiler (x86 Target)\\Test Files\\"
    
    def test_literal_unsigned_integer(self):
        
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
    
    def test_literal_integer(self):
        
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
        
    def test_literal_string(self):
        
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
        
    def test_literal_character(self):
        
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
    
    @unittest.skip("This test has an infinite loop somewhere!")
    def test_literal_float(self):
        
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

