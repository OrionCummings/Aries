import returns
from ISA import SAISA, Instruction

class Program():
    
    def __init__(Self, Filename: str, EntryPoint = 0) -> None:
        Self.Filename: str = Filename
        Self.EntryPoint: int = EntryPoint
        Self.SizeInBytes: int = 0
        Self.Contents: str = ""
        Self.ISA: SAISA = SAISA()
        
        Self.Read()
    
    def __str__(Self) -> str:
        Builder: str = ""
        Builder += "\n[" + Self.Filename + " - " + str(Self.SizeInBytes) + " Bytes]\n"
        if len(Self.Contents) < 1:
            Builder += "No File Contents"
        else:
            Builder += Self.Contents
        return Builder
    
    def Print(Self):
        print(Self)
    
    def Parse(Self, Line: str) -> str:
        RInstruction = Self.ISA.ParseInstruction(Line)
        
        try:
            I: Instruction = RInstruction.unwrap()
        except returns.primitives.exceptions.UnwrapFailedError:
            print("Invalid instruction found!")
            exit(1)
        
        return str(I)
    
    def Read(Self) -> bool:
        try:
            with open(Self.Filename, "r") as File:
                while Line := File.readline():
                    Self.Contents += Self.Parse(Line) + "\n"
                    Self.SizeInBytes += 8
        except FileNotFoundError:
            print("File '" + Self.Filename + "' not found! Unable to parse program")
            return False
        return True

if __name__ == "__main__":
    
    P: Program = Program("Simple.aria")
    P.Print()