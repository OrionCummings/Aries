
from typing import List

from option import Err, Ok, Result

from PrettyPrinting import PP

# The number of memory entries to show per line when printed
MEMORY_DISPLAY_LENGTH = 4

class Memory():
    
    def __init__(Self, Capacity: int):
        Self.Memory: list[int] = list(0 for _ in range(0, Capacity))
        Self.Capacity = Capacity
        Self.Size = 0
    
    def __str__(Self) -> str:
        Builder: str = ""
        for Index in range(0, Self.Capacity):
            
            if Index != 0 and Index % MEMORY_DISPLAY_LENGTH == 0:
                Builder += "\n"
            
            if Index >= Self.Size: Builder += PP.Bold(str(Self.Memory[Index]))
            else: Builder += str(Self.Memory[Index])
            
            Builder += " "

        return Builder
    
    def __getitem__(Self, Index: int) -> int:
        return Self.Memory[Index]
    
    def Update(Self, Value: int, Index: int) -> Result[bool, str]:
        if Index < 0: return Err("Memory location out of bounds: {} < 0".format(Index))
        if Index >= Self.Capacity: return Err("Memory location out of bounds: {} > {}".format(Index, Self.Capacity))
        
        Self.Memory[Index] = Value
        if Index > Self.Size: Self.Size = Index
        
        return Ok(True)
    
    def UpdateChunk(Self, Values: list[int], Index: int) -> Result[bool, str]:
        if len(Values) == 0: return Err("No values to write!")
        if Index < 0: return Err("Memory location out of bounds: {} < 0!".format(Index))
        if Index >= Self.Capacity: return Err("Memory location out of bounds: {} > {}!".format(Index, Self.Capacity))
        if Index + len(Values) >= Self.Capacity: return Err("Memory location will be out of bounds: {} > {}!".format(Index, Self.Capacity))
        
        Self.Memory[Index:Index + len(Values)] = Values
        if Index + len(Values) > Self.Size: Self.Size = Index + len(Values)

        return Ok(True)
        