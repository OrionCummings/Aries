import inspect
from typing import List
import unittest

from Tokenizer import Token, TokenType, Tokenizer

class TokenizerUnitTests(unittest.TestCase):

    UnitTestResultDirectory = "Unit Test Results/"

    def WriteResults(Self, Expected, Actual):
        
        FileExpected = open(Self.UnitTestResultDirectory + inspect.currentframe().f_back.f_code.co_name + "Expected.txt", 'w')
        FileActual   = open(Self.UnitTestResultDirectory + inspect.currentframe().f_back.f_code.co_name +   "Actual.txt", 'w')
        
        for A in Actual:
            FileActual.write(str(A) + '\n')
        
        for E in Expected:
            FileExpected.write(str(E) + '\n')
            
        FileActual.close()
        FileExpected.close()

    def test_Peek(Self):
        """Tokenization Test: Peek"""
        
        T = Tokenizer("Source Files\\minimal.ari")
        
        P = T.Peek(-37)
        Self.assertIsNone(P)
        
        P = T.Peek(0)
        Self.assertIsNone(P)
                
        P = T.Peek()
        Self.assertEqual(P, 'd')
                
        P = T.Peek(1)
        Self.assertEqual(P, 'd')
                
        P = T.Peek(3)
        Self.assertEqual(P, 'def')
                
        P = T.Peek(300)
        Self.assertIsNone(P)
        
    def test_Pop(Self):
        """Tokenization Test: Pop"""
        T = Tokenizer("Source Files\\minimal.ari")
        
        P = T.Pop(-37)
        Self.assertIsNone(P)
        
        P = T.Pop(0)
        Self.assertIsNone(P)
                
        P = T.Pop()
        Self.assertEqual(P, 'd')
        Self.assertEqual(T.Index, 1)
                
        P = T.Pop(1)
        Self.assertEqual(P, 'e')
        Self.assertEqual(T.Index, 2)
                
        P = T.Pop(6)
        Self.assertEqual(P, 'f main')
        Self.assertEqual(T.Index, 8)
                
        P = T.Pop(300)
        Self.assertIsNone(P)
        
    def test_Minimal(Self):
        """Tokenization Test: minimal.ari"""
        
        T = Tokenizer("Source Files\\minimal.ari")
        T.Tokenize()
        
        ExpectedTokenList: List[Token] = [
            Token(Type = TokenType.KEYWORD_DEF,         Line = 1, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 1, Value = "main"),
            Token(Type = TokenType.PUNC_PAREN_OPEN,     Line = 1, Value = None),
            Token(Type = TokenType.PUNC_PAREN_CLOSE,    Line = 1, Value = None),
            Token(Type = TokenType.ARROW,               Line = 1, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 1, Value = "int"),
            Token(Type = TokenType.PUNC_BRACE_OPEN,     Line = 1, Value = None),
            Token(Type = TokenType.KEYWORD_RETURN,      Line = 2, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 2, Value = "0"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 2, Value = None),
            Token(Type = TokenType.PUNC_BRACE_CLOSE,    Line = 3, Value = None),
            Token(Type = TokenType.EOF,                 Line = 3, Value = None)
        ]
        
        Self.WriteResults(Expected = ExpectedTokenList, Actual = T.Tokens)
        Self.assertListEqual(ExpectedTokenList, T.Tokens)

    def test_Return(Self):
        """Tokenization Test: return.ari"""
        
        T = Tokenizer("Source Files\\return.ari")
        T.Tokenize()
        
        ExpectedTokenList: List[Token] = [
            Token(Type = TokenType.KEYWORD_DEF,         Line = 1, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 1, Value = "main"),
            Token(Type = TokenType.PUNC_PAREN_OPEN,     Line = 1, Value = None),
            Token(Type = TokenType.PUNC_PAREN_CLOSE,    Line = 1, Value = None),
            Token(Type = TokenType.ARROW,               Line = 1, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 1, Value = "int"),
            Token(Type = TokenType.PUNC_BRACE_OPEN,     Line = 1, Value = None),
            Token(Type = TokenType.KEYWORD_RETURN,      Line = 2, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 2, Value = "27"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 2, Value = None),
            Token(Type = TokenType.PUNC_BRACE_CLOSE,    Line = 3, Value = None),
            Token(Type = TokenType.EOF,                 Line = 3, Value = None)
        ]
        
        Self.WriteResults(Expected = ExpectedTokenList, Actual = T.Tokens)
        Self.assertListEqual(ExpectedTokenList, T.Tokens)

    def test_Operators(Self):
        """Tokenization Test: operators.ari"""
        
        T = Tokenizer("Source Files\\operators.ari")
        T.Tokenize()
        
        ExpectedTokenList: List[Token] = [
            Token(Type = TokenType.KEYWORD_DEF,         Line = 1, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 1, Value = "main"),
            Token(Type = TokenType.PUNC_PAREN_OPEN,     Line = 1, Value = None),
            Token(Type = TokenType.PUNC_PAREN_CLOSE,    Line = 1, Value = None),
            Token(Type = TokenType.ARROW,               Line = 1, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 1, Value = "int"),
            Token(Type = TokenType.PUNC_BRACE_OPEN,     Line = 1, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 3, Value = "int"),
            Token(Type = TokenType.IDENTIFIER,          Line = 3, Value = "A"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 3, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 3, Value = "3"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 3, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 4, Value = "int"),
            Token(Type = TokenType.IDENTIFIER,          Line = 4, Value = "B"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 4, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 4, Value = "5"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 4, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 6, Value = "bool"),
            Token(Type = TokenType.IDENTIFIER,          Line = 6, Value = "C"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 6, Value = None),
            Token(Type = TokenType.KEYWORD_FALSE,       Line = 6, Value = None),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 6, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 7, Value = "bool"),
            Token(Type = TokenType.IDENTIFIER,          Line = 7, Value = "D"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 7, Value = None),
            Token(Type = TokenType.KEYWORD_TRUE,        Line = 7, Value = None),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 7, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 9, Value = "uint"),
            Token(Type = TokenType.IDENTIFIER,          Line = 9, Value = "E"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 9, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 9, Value = "10"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 9, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 10, Value = "uint"),
            Token(Type = TokenType.IDENTIFIER,          Line = 10, Value = "F"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 10, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 10, Value = "0b010010"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 10, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 12, Value = "int"),
            Token(Type = TokenType.IDENTIFIER,          Line = 12, Value = "a1"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 12, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 12, Value = "A"),
            Token(Type = TokenType.OP_PLUS,             Line = 12, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 12, Value = "B"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 12, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 13, Value = "int"),
            Token(Type = TokenType.IDENTIFIER,          Line = 13, Value = "a2"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 13, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 13, Value = "A"),
            Token(Type = TokenType.OP_DASH,             Line = 13, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 13, Value = "B"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 13, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 14, Value = "int"),
            Token(Type = TokenType.IDENTIFIER,          Line = 14, Value = "a3"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 14, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 14, Value = "A"),
            Token(Type = TokenType.OP_SLASH,            Line = 14, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 14, Value = "B"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 14, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 15, Value = "int"),
            Token(Type = TokenType.IDENTIFIER,          Line = 15, Value = "a4"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 15, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 15, Value = "A"),
            Token(Type = TokenType.OP_STAR,             Line = 15, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 15, Value = "B"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 15, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 16, Value = "int"),
            Token(Type = TokenType.IDENTIFIER,          Line = 16, Value = "a5"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 16, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 16, Value = "A"),
            Token(Type = TokenType.OP_PERCENT,          Line = 16, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 16, Value = "B"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 16, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 18, Value = "bool"),
            Token(Type = TokenType.IDENTIFIER,          Line = 18, Value = "b0"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 18, Value = None),
            Token(Type = TokenType.OP_NOT,              Line = 18, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 18, Value = "C"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 18, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 19, Value = "bool"),
            Token(Type = TokenType.IDENTIFIER,          Line = 19, Value = "b1"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 19, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 19, Value = "C"),
            Token(Type = TokenType.OP_EQUIVALENCE,      Line = 19, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 19, Value = "D"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 19, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 20, Value = "bool"),
            Token(Type = TokenType.IDENTIFIER,          Line = 20, Value = "b2"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 20, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 20, Value = "C"),
            Token(Type = TokenType.OP_NONEQUIVALENCE,   Line = 20, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 20, Value = "D"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 20, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 21, Value = "bool"),
            Token(Type = TokenType.IDENTIFIER,          Line = 21, Value = "b3"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 21, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 21, Value = "C"),
            Token(Type = TokenType.OP_LT,               Line = 21, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 21, Value = "D"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 21, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 22, Value = "bool"),
            Token(Type = TokenType.IDENTIFIER,          Line = 22, Value = "b4"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 22, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 22, Value = "C"),
            Token(Type = TokenType.OP_LTE,              Line = 22, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 22, Value = "D"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 22, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 23, Value = "bool"),
            Token(Type = TokenType.IDENTIFIER,          Line = 23, Value = "b5"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 23, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 23, Value = "C"),
            Token(Type = TokenType.OP_GT,               Line = 23, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 23, Value = "D"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 23, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 24, Value = "bool"),
            Token(Type = TokenType.IDENTIFIER,          Line = 24, Value = "b6"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 24, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 24, Value = "C"),
            Token(Type = TokenType.OP_GTE,              Line = 24, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 24, Value = "D"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 24, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 25, Value = "bool"),
            Token(Type = TokenType.IDENTIFIER,          Line = 25, Value = "b7"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 25, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 25, Value = "C"),
            Token(Type = TokenType.OP_AND,              Line = 25, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 25, Value = "D"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 25, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 26, Value = "bool"),
            Token(Type = TokenType.IDENTIFIER,          Line = 26, Value = "b8"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 26, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 26, Value = "C"),
            Token(Type = TokenType.OP_OR,               Line = 26, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 26, Value = "D"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 26, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 28, Value = "uint"),
            Token(Type = TokenType.IDENTIFIER,          Line = 28, Value = "c1"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 28, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 28, Value = "E"),
            Token(Type = TokenType.OP_BIT_AND,          Line = 28, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 28, Value = "F"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 28, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 29, Value = "uint"),
            Token(Type = TokenType.IDENTIFIER,          Line = 29, Value = "c2"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 29, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 29, Value = "E"),
            Token(Type = TokenType.OP_BIT_OR,           Line = 29, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 29, Value = "F"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 29, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 30, Value = "uint"),
            Token(Type = TokenType.IDENTIFIER,          Line = 30, Value = "c3"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 30, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 30, Value = "E"),
            Token(Type = TokenType.OP_BIT_XOR,          Line = 30, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 30, Value = "F"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 30, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 31, Value = "uint"),
            Token(Type = TokenType.IDENTIFIER,          Line = 31, Value = "c4"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 31, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 31, Value = "E"),
            Token(Type = TokenType.OP_SL,               Line = 31, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 31, Value = "1"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 31, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 32, Value = "uint"),
            Token(Type = TokenType.IDENTIFIER,          Line = 32, Value = "c5"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 32, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 32, Value = "1"),
            Token(Type = TokenType.OP_SR,               Line = 32, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 32, Value = "4"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 32, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 33, Value = "uint"),
            Token(Type = TokenType.IDENTIFIER,          Line = 33, Value = "c6"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 33, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 33, Value = "4"),
            Token(Type = TokenType.OP_RL,               Line = 33, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 33, Value = "1"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 33, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 34, Value = "uint"),
            Token(Type = TokenType.IDENTIFIER,          Line = 34, Value = "c7"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 34, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 34, Value = "1"),
            Token(Type = TokenType.OP_RR,               Line = 34, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 34, Value = "4"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 34, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 36, Value = "int"),
            Token(Type = TokenType.IDENTIFIER,          Line = 36, Value = "d1"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 36, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 36, Value = "A"),
            Token(Type = TokenType.OP_INC,              Line = 36, Value = None),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 36, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 37, Value = "int"),
            Token(Type = TokenType.IDENTIFIER,          Line = 37, Value = "d2"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 37, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 37, Value = "B"),
            Token(Type = TokenType.OP_DEC,              Line = 37, Value = None),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 37, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 39, Value = "d1"),
            Token(Type = TokenType.OP_ADD_ASSIGN,       Line = 39, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 39, Value = "5"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 39, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 40, Value = "d1"),
            Token(Type = TokenType.OP_SUB_ASSIGN,       Line = 40, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 40, Value = "5"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 40, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 41, Value = "d1"),
            Token(Type = TokenType.OP_MUL_ASSIGN,       Line = 41, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 41, Value = "5"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 41, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 42, Value = "d1"),
            Token(Type = TokenType.OP_DIV_ASSIGN,       Line = 42, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 42, Value = "5"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 42, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 43, Value = "d1"),
            Token(Type = TokenType.OP_MOD_ASSIGN,       Line = 43, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 43, Value = "5"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 43, Value = None),
            
            Token(Type = TokenType.KEYWORD_RETURN,      Line = 45, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 45, Value = "0"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 45, Value = None),
            Token(Type = TokenType.PUNC_BRACE_CLOSE,    Line = 46, Value = None),
            Token(Type = TokenType.EOF,                 Line = 46, Value = None),
        ]
        
        Self.WriteResults(Expected = ExpectedTokenList, Actual = T.Tokens)
        Self.assertListEqual(ExpectedTokenList, T.Tokens)

    #@unittest.skip("Feature not fully implemented")
    def test_Variables(Self):
        """Tokenization Test: variables.ari"""
        
        T = Tokenizer("Source Files\\variables.ari")
        T.Tokenize()
        
        ExpectedTokenList: List[Token] = [
            Token(Type = TokenType.KEYWORD_DEF,         Line = 1, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 1, Value = "main"),
            Token(Type = TokenType.PUNC_PAREN_OPEN,     Line = 1, Value = None),
            Token(Type = TokenType.PUNC_PAREN_CLOSE,    Line = 1, Value = None),
            Token(Type = TokenType.ARROW,               Line = 1, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 1, Value = "int"),
            Token(Type = TokenType.PUNC_BRACE_OPEN,     Line = 1, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 3, Value = "int"),
            Token(Type = TokenType.IDENTIFIER,          Line = 3, Value = "a"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 3, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 4, Value = "uint"),
            Token(Type = TokenType.IDENTIFIER,          Line = 4, Value = "b"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 4, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 4, Value = "5"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 4, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 5, Value = "char"),
            Token(Type = TokenType.OP_STAR,             Line = 5, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 5, Value = "c"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 3, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 5, Value = "0x2"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 5, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 6, Value = "char"),
            Token(Type = TokenType.IDENTIFIER,          Line = 6, Value = "d"),
            Token(Type = TokenType.PUNC_BRACKET_OPEN,   Line = 6, Value = None),
            Token(Type = TokenType.PUNC_BRACKET_CLOSE,  Line = 6, Value = None),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 6, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 6, Value = "0xFF0"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 6, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 7, Value = "char"),
            Token(Type = TokenType.IDENTIFIER,          Line = 7, Value = "e"),
            Token(Type = TokenType.PUNC_BRACKET_OPEN,   Line = 7, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 7, Value = "4"),
            Token(Type = TokenType.PUNC_BRACKET_CLOSE,  Line = 7, Value = None),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 7, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 8, Value = "float"),
            Token(Type = TokenType.IDENTIFIER,          Line = 8, Value = "f"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 8, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 9, Value = "float"),
            Token(Type = TokenType.IDENTIFIER,          Line = 9, Value = "g"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 9, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 9, Value = "5.24"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 9, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 10, Value = "void"),
            Token(Type = TokenType.OP_STAR,             Line = 10, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 10, Value = "h"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 10, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 10, Value = "0x17"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 10, Value = None),

            Token(Type = TokenType.IDENTIFIER,          Line = 11, Value = "int"),
            Token(Type = TokenType.OP_STAR,             Line = 11, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 11, Value = "i"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 11, Value = None),
            Token(Type = TokenType.OP_BIT_AND,          Line = 11, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 11, Value = "a"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 11, Value = None),

            Token(Type = TokenType.IDENTIFIER,          Line = 12, Value = "int"),
            Token(Type = TokenType.IDENTIFIER,          Line = 12, Value = "x"),
            Token(Type = TokenType.PUNC_COMMA,          Line = 12, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 12, Value = "y"),
            Token(Type = TokenType.PUNC_COMMA,          Line = 12, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 12, Value = "z"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 12, Value = None),

            Token(Type = TokenType.IDENTIFIER,          Line = 13, Value = "int"),
            Token(Type = TokenType.IDENTIFIER,          Line = 13, Value = "l"),
            Token(Type = TokenType.PUNC_COMMA,          Line = 13, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 13, Value = "m"),
            Token(Type = TokenType.PUNC_COMMA,          Line = 13, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 13, Value = "n"),
            Token(Type = TokenType.PUNC_COMMA,          Line = 13, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 13, Value = "o"),
            Token(Type = TokenType.PUNC_COMMA,          Line = 13, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 13, Value = "p"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 13, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 13, Value = "5"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 13, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 14, Value = "bool"),
            Token(Type = TokenType.IDENTIFIER,          Line = 14, Value = "tesjio"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 13, Value = None),
            Token(Type = TokenType.KEYWORD_FALSE,       Line = 13, Value = None),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 14, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 15, Value = "bool"),
            Token(Type = TokenType.IDENTIFIER,          Line = 15, Value = "gdf"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 13, Value = None),
            Token(Type = TokenType.KEYWORD_TRUE,        Line = 13, Value = None),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 15, Value = None),

            Token(Type = TokenType.KEYWORD_RETURN,      Line = 15, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 15, Value = "2"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 15, Value = None),
            
            Token(Type = TokenType.PUNC_BRACE_CLOSE,    Line = 16, Value = None),
            Token(Type = TokenType.EOF,                 Line = 16, Value = None)
        ]
        
        Self.WriteResults(Expected = ExpectedTokenList, Actual = T.Tokens)
        Self.assertListEqual(ExpectedTokenList, T.Tokens)

    def test_Literals(Self):
        """Tokenization Test: literals.ari"""
        
        T = Tokenizer("Source Files\\literals.ari")
        T.Tokenize()
        
        ExpectedTokenList: List[Token] = [
            Token(Type = TokenType.KEYWORD_DEF,         Line = 1, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 1, Value = "main"),
            Token(Type = TokenType.PUNC_PAREN_OPEN,     Line = 1, Value = None),
            Token(Type = TokenType.PUNC_PAREN_CLOSE,    Line = 1, Value = None),
            Token(Type = TokenType.ARROW,               Line = 1, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 1, Value = "int"),
            Token(Type = TokenType.PUNC_BRACE_OPEN,     Line = 1, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 3, Value = "int"),
            Token(Type = TokenType.IDENTIFIER,          Line = 3, Value = "a"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 3, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 3, Value = "472"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 3, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 4, Value = "int"),
            Token(Type = TokenType.IDENTIFIER,          Line = 4, Value = "b"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 4, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 4, Value = "0xDEADBEEF"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 4, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 5, Value = "uint"),
            Token(Type = TokenType.IDENTIFIER,          Line = 5, Value = "c"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 5, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 5, Value = "0o15236274"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 5, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 6, Value = "uint"),
            Token(Type = TokenType.IDENTIFIER,          Line = 6, Value = "d"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 6, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 6, Value = "0b01001011"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 6, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 7, Value = "float"),
            Token(Type = TokenType.IDENTIFIER,          Line = 7, Value = "e"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 7, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 7, Value = "1982.156"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 7, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 8, Value = "bool"),
            Token(Type = TokenType.IDENTIFIER,          Line = 8, Value = "f"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 8, Value = None),
            Token(Type = TokenType.KEYWORD_TRUE,        Line = 8, Value = None),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 8, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 9, Value = "bool"),
            Token(Type = TokenType.IDENTIFIER,          Line = 9, Value = "g"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 9, Value = None),
            Token(Type = TokenType.KEYWORD_FALSE,       Line = 9, Value = None),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 9, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 10, Value = "char"),
            Token(Type = TokenType.IDENTIFIER,          Line = 10, Value = "h"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 10, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 10, Value = "'h'"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 10, Value = None),
            
            Token(Type = TokenType.IDENTIFIER,          Line = 11, Value = "char"),
            Token(Type = TokenType.OP_STAR,             Line = 11, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 11, Value = "i"),
            Token(Type = TokenType.OP_ASSIGNMENT,       Line = 11, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 11, Value = '"test string"'),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 11, Value = None),
            
            Token(Type = TokenType.KEYWORD_RETURN,      Line = 13, Value = None),
            Token(Type = TokenType.IDENTIFIER,          Line = 13, Value = "17"),
            Token(Type = TokenType.PUNC_SEMICOLON,      Line = 13, Value = None),
            Token(Type = TokenType.PUNC_BRACE_CLOSE,    Line = 14, Value = None),
            Token(Type = TokenType.EOF,                 Line = 14, Value = None)
        ]
        
        Self.WriteResults(Expected = ExpectedTokenList, Actual = T.Tokens)
        Self.assertListEqual(ExpectedTokenList, T.Tokens)
        
if __name__ == '__main__':
    unittest.main()