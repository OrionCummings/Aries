import argparse
from enum import Enum
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
        
    
    # Tokenize the source file
    T: Tokenizer = Tokenizer(RSetup.unwrap().Source)
    TResult: Result[int, str] = T.Tokenize()
    
    # DEBUG
    # print(T)
    
    match TResult:
        case Success(_):
            print(PP.GreenBold("Tokenization success!"))
            print(T)
        case Failure(X):
            print(PP.RedBold("Tokenization failure!"))
            print(str(X))
            return CompilerErrorCode.ExitFailureTokenizer
    
    # Parse the tokens
    A: AST = AST(T)
    
    # Generate the assembly instructions
    G: Generator = Generator(A, "x86")

def Setup() -> Result[str, int]:
    
    # Verify command line arguments
    ArgumentParser = argparse.ArgumentParser()
    ArgumentParser.add_argument('Source', metavar='s', type=str, help="The source file to compile.")
    ArgumentParser.add_argument('--Target', metavar='t', type=str, default="x86", help="The target architecture: x86, Aries")
    try:
        Arguments = ArgumentParser.parse_args()
    except SystemExit:
        print("Incorrect usage!")
        return CompilerErrorCode.ExitFailureCLI
    except:
        print("Unknown CLI error!")
        return CompilerErrorCode.ExitFailureCLI
    
    return Arguments

if __name__ == "__main__":
    print()
    Main()
    print()