from option import Err, Ok, Result
from Constants import *

class RegisterFile():
    
    def __init__(Self):
        """Creates an empty RegisterFile."""
        
        Self.Registers = {}
        for R in REGISTERS.keys():
            Self.Registers[R] = 0
    
    def __eq__(Self, Other):
        
        if not isinstance(Other, RegisterFile):
            raise NotImplementedError
        
        for S, O in zip(Self.Registers.items(), Other.Registers.items()):
            if not S == O:
                return False
            
        return True
        
    def __str__(Self) -> str:
        """Returns a string representation of a RegisterFile."""
        Builder = ""
        for R in Self.Registers.items():
            Builder += ("{:2} = {:032b}".format(R[0], R[1]))
            Builder += "\n"
        Builder += "                             HTIOSPCZ"
        return Builder
    
    def SetReg(Self, Reg: str, Value: int) -> None:
        if Reg in Self.Registers:
            Self.Registers[Reg] = Value & 0xFFFFFFFF
    
    def GetReg(Self, Reg: str) -> Result[int, str]:
        if Reg in Self.Registers:
            return Ok(Self.Registers[Reg])
        return Err("No register with key '{}'!".format(Reg))
    
    def GetPC(Self) -> int:
        return Self.Registers["PC"]
    
    def IncrementProgramCounter(Self) -> None:
        Self.Registers['PC'] += PC_INC
    
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
    
    RF.SetReg("B", 255)
    RF.SetReg("G", 16000)
    RF.SetReg("H", 2367471)
    print(RF)
    
    print(RF.GetReg("A").unwrap())
    print(RF.GetReg("B").unwrap())
    print(RF.GetReg("G").unwrap())
    print(RF.GetReg("H").unwrap())
    
    
    