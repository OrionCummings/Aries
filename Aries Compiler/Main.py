import argparse
from enum import Enum
from returns.result import Result, Success, Failure
from Tokenizer import Tokenizer

class ProgramErrorCode(Enum):
    ExitFailure = -1,
    ExitSuccess = 0,
    ExitFailureCLI = 1,
    ExitFailureTokenizer = 2,
    ExitFailureParser = 3,
    ExitFailureGenerator = 4

def Main():
    
    # Verify command line arguments
    ArgumentParser = argparse.ArgumentParser()
    ArgumentParser.add_argument('Source', type=str)
    try:
        Arguments = ArgumentParser.parse_args()
    except SystemExit:
        print("Incorrect usage!")
        return ProgramErrorCode.ExitFailureCLI
    except:
        print("Unknown CLI error!")
        return ProgramErrorCode.ExitFailureCLI
    
    # Tokenize the source file
    T: Tokenizer = Tokenizer(Arguments.Source)
    TResult: Result[int, str] = T.Tokenize()
    
    match TResult:
        
        case Success(_):
            print("Tokenization success!")
            
        case Failure(X):
            print("Tokenization failure!")
            print(str(X))
            return ProgramErrorCode.ExitFailureTokenizer
    
    # Parse the tokens
    
    
    # Generate the assembly instructions
    

if __name__ == "__main__":
    Main()