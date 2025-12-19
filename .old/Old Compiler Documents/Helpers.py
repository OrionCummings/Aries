from inspect import getouterframes
import sys

def Stack(context=1):
    """Return a list of records for the stack above the caller's frame.
    https://stackoverflow.com/questions/900392/getting-the-caller-function-name-inside-another-function-in-python"""
    return getouterframes(sys._getframe(1), context)

def GetCurrentFunction() -> (str, int):
    Frame = Stack(1)[2]
    return (Frame.function, Frame.lineno)

class Debug:
    def Error() -> str:
        (FunctionName, LineNumber) = GetCurrentFunction()
        return "[" + FunctionName + ":" + str(LineNumber) + "] "