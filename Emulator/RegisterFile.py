from Constants import *

class RegisterFile():
    
    def __init__(Self):
        """Creates an empty RegisterFile."""
        
        Self.Registers = {}
        for R in REGISTERS.keys():
            Self.Registers[R] = 0
    
    def __str__(Self) -> str:
        """Returns a string representation of a RegisterFile."""
        Builder = ""
        for R in Self.Registers.items():
            Builder += ("{:2} = {:016b}".format(R[0], R[1]))
            Builder += "\n"
        Builder += "            HTDIOSPCZ"
        return Builder
    
    def SetReg(Self, Reg: str, Value: int) -> None:
        if Reg in Self.Registers:
            Self.Registers[Reg] = Value
    
    def GetReg(Self, Reg: str) -> int:
        if Reg in Self.Registers:
            return Self.Registers[Reg]
        return None
    
    def IncrementInstructionPointer(Self) -> None:
        Self.Registers['IP'] += IP_INC
    
    def IncrementBasePointer(Self) -> None:
        Self.Registers['BP'] += BP_INC
    
    def IncrementStackPointer(Self) -> None:
        Self.Registers['SP'] += SP_INC
    
    def ClearFlags(Self) -> None:
        Self.Registers['FL'] = 0
    
    def SetFlag(Self, Flag: int) -> None:
        Self.Registers['FL'] = SetBit(Self.Registers['FL'], Flag)
    
    def GetFlag(Self, Flag: int) -> bool:
        return GetBit(Self.Registers['FL'], Flag)
    
    def ToggleFlag(Self, Flag: int) -> None:
        Self.Registers['FL'] = ToggleBit(Self.Registers['FL'], Flag)
    
if __name__ == "__main__":
    
    RF = RegisterFile()
    print(RF)
    print()

