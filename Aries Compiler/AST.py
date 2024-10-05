from dataclasses import dataclass
from typing import List
from  Tokenizer import Tokenizer, Token

class ASTNode():
    """An AST node. A base class for expression and statement nodes."""

    def __init__(Self, Type: str = None, Start: int = None, End: int = None):
        Self.Type: str  = Type
        Self.Start: int = Start
        Self.End: int   = End
        Self.Body       = []

    def __str__(Self)-> str:
        Builder: str = ""
        Builder += ""
        return Builder

class AST():
    """An Abstract Syntax Tree."""
    
    def __init__(Self, Tokenizer: Tokenizer):
        Self.FilePath: str      = Tokenizer.FilePath
        Self.Tokenizer          = Tokenizer
        Self.Root: ASTNode      = Self.Parse()
    
    # def __str__(Self) -> str:
        # print(Self.Root)
        # [print(Node) for Node in Self.Root.Children]
    
    def ParseExpression(Self):
        pass
    
    def Parse(Self) -> ASTNode:
        
        # Create the root program node
        Root: ASTNode = ASTNode(type="Program", Start=0, End=Self.Tokenizer.SourceFileContentsLength)
        
        # While there are tokens left to parse
        while not Self.Tokenizer.Tokens:
            
            # Get the next token
            NextToken: Token = Self.Tokenizer.Tokens.pop(0)
            
            print(NextToken)
        
        # Return the root program node
        return Root
