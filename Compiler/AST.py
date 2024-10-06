from dataclasses import dataclass
from returns.result import Result, Success, Failure
from typing import List, Optional
from PrettyPrinting import PP
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
    #     Builder: str = ""
    #     Builder += str(Self.Root)
    #     [Builder.append(N) for N in Self.Root.Body]
    #     return Builder
    
    @dataclass
    class VariableDeclaration():
        """ 
        A variable declaration. Examples:
        int x = 4;
        float y[6];
        char z[] = { 't', 'e', 's', 't', '\n' };
        char s[] = z;
        uint a, b, c = 2;
        float a, b, c;
        """
        Type: Token                 = None
        Identifiers: List[Token]    = None
        Length: int                 = 0
        Expression: Optional[List[str]]  = None
    
    @dataclass
    class FunctionDeclaration():
        """
        A function definition. Examples:
        def f() {
            // ...
        }
        def overload g(int x) -> bool {
            // ...
        }
        """
        Identifier: Token               = None
        ReturnType: Token               = None
        Parameters: Optional[List[str]] = None
        Body: Optional[str]             = None
    
    @dataclass
    class Declaration():
        VarDecl:  VariableDeclaration = None
        FuncDecl: FunctionDeclaration = None
    
    def ParseVariableDeclaration(Self) -> Result[VariableDeclaration, str]:
        VarDecl: VariableDeclaration = None
        
        return Failure("Failed to parse variable declaration")
        
    def ParseFunctionDeclaration(Self) -> Result[FunctionDeclaration, str]:
        FuncDecl: FunctionDeclaration = None
        
        return Failure("Failed to parse function declaration")
    
    def ParseDeclaration(Self) -> Result[Declaration, str]:
        
        # Try to parse a variable declaration
        RVariable = Self.ParseVariableDeclaration()
        if RVariable.value_or(None) is not None:
            Variable = RVariable.unwrap()
            return Variable
        
        # Try to parse a function declaration
        RFunction = Self.ParseFunctionDeclaration()
        if RFunction.value_or(None) is not None:
            Function = RFunction.unwrap()
            return Function
            
        return Failure("Failed to parse a declaration")
            
    def Parse(Self) -> ASTNode:
        
        # Create the root program node
        Root: ASTNode = ASTNode(type="Program", Start=0, End=Self.Tokenizer.SourceFileContentsLength)
        
        # While there are tokens left to parse
        while not Self.Tokenizer.Tokens:
            
            # Try to parse a declaration
            RDeclaration = Self.ParseDeclaration()
            if RDeclaration.value_or(None) is not None:
                print(RDeclaration.unwrap())
            else:
                print(PP.RedBold("Invalid declaration on line {}".format("???")))
            
        
        # Return the root program node
        return Root
