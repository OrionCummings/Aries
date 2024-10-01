from typing import List
import returns
from ISA import SAISA, Instruction

class Program():
    
    def __init__(Self, Filename: str, EntryPoint = 0) -> None:
        Self.Filename: str = Filename
        Self.EntryPoint: int = EntryPoint
        Self.SizeInBytes: int = 0
        Self.Bytes: bytearray = bytearray()
        Self.ISA: SAISA = SAISA()
        Self.SetISA("SAISA")
        Self.Read()
    
    def __str__(Self) -> str:
        Builder: str = ""
        Builder += "\n[" + Self.Filename + " - " + str(Self.SizeInBytes) + " Bytes]\n"
        if len(Self.Bytes) < 1:
            Builder = "No File Contents"
        else:
            for Byte in Self.Bytes:
                Builder += str(Byte)
        return Builder
    
    def Print(Self):
        print(Self)
    
    def SetISA(Self, ISA: str):
        match ISA:
            case "SAISA":
                Self.ISA = SAISA()
            case "BAISA":
                print("Unimplemented ISA '{}' provided".format(ISA))
            case "FAISA":
                print("Unimplemented ISA '{}' provided".format(ISA))
            case _:
                print("Invalid ISA '{}' provided".format(ISA))
    
    def ParseIntoBytes(Self, Line: str) -> List[int]:
        
        # Given the ISA, parse the instruction
        RInstruction = Self.ISA.ParseInstruction(Line)
        
        # Ensure this instruction was properly parsed
        try:
            I: Instruction = RInstruction.unwrap()
        except returns.primitives.exceptions.UnwrapFailedError:
            print("Invalid instruction found!")
            exit(1)
        
        return I.AsBytes()
    
    def Read(Self) -> bool:
        try:
            with open(Self.Filename, "r") as File:
                while Line := File.readline():
                    Self.Bytes.extend(Self.ParseIntoBytes(Line))
                    Self.SizeInBytes += 8
        except FileNotFoundError:
            print("File '" + Self.Filename + "' not found! Unable to parse program")
            return False
        return True

# if __name__ == "__main__":
    
#     P: Program = Program("Simple.aria")
#     P.Print()