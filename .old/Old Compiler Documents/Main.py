import argparse
from enum import Enum
import unittest
from returns.result import Result, Success, Failure
from AST import AST
from Generator import Generator
from PrettyPrinting import PP
from Tokenizer import Tokenizer

class CompilerErrorCode(Enum):
    ExitFailure = -1,
    ExitSuccess = 0,
    ExitFailureCLI = 1,
    ExitFailureFile = 2,
    ExitFailureTokenizer = 3,
    ExitFailureParser = 4,
    ExitFailureGenerator = 5

def Main():
    
    RSetup = Setup()
    if RSetup.value_or(None) is None:
        print(RSetup.failure())
        exit(CompilerErrorCode.ExitFailureTokenizer)
        
    Arguments = RSetup.unwrap()
    
    # Tokenize the source file
    T: Tokenizer = Tokenizer(Arguments.Source)
    TResult: Result[int, str] = T.Tokenize()
    
    match TResult:
        case Success(_):
            print(PP.GreenBold("Tokenization success!"))
            print(T)
        case Failure(X):
            print(PP.RedBold("Tokenization failure!"))
            print(str(X))
            exit(CompilerErrorCode.ExitFailureTokenizer)
    
    # Parse the tokens
    #A: AST = AST(T)
    
    # Generate the assembly instructions
    #G: Generator = Generator(A, "x86")

def Setup() -> Result[str, int]:
    
    # Verify command line arguments
    ArgumentParser = argparse.ArgumentParser()
    ArgumentParser.add_argument('Source', metavar='s', type=str, help="The source file to compile.")
    ArgumentParser.add_argument('--Target', metavar='t', type=str, default="x86", help="The target architecture: x86, Aries")
    try:
        Arguments = ArgumentParser.parse_args()
    except SystemExit:
        return Failure("Incorrect usage!")
    except:
        return Failure("Unknown CLI error!")
    
    return Success(Arguments)

if __name__ == "__main__":
    print()
    Main()
    print()