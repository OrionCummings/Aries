
from Constants import GetBit, SetBit, ToggleBit


class Flags():
    """Contains all information regarding CPU flags and the functions to manipulate them."""
    
    def __init__(Self):
        Self.Flag: int          = 0
        Self.PreviousFlag: int  = 0
    
    def __str__(Self):
        Builder: str = ""
        Builder += str(Self.Flag)
        return Builder
    
    # TODO: Probably want to do something else!!!!
    def Tick(Self) -> None:
        Self.PreviousFlag = Self.Flag
    
    def GetFlag(Self, FlagIndex: int) -> int:
        return GetBit(Self.Flag, FlagIndex)
    
    def SetFlag(Self, FlagIndex: int) -> int:
        return SetBit(Self.Flag, FlagIndex)
    
    def ToggleFlag(Self, FlagIndex: int) -> int:
        return ToggleBit(Self.Flag, FlagIndex)
    
    
    