from __future__ import annotations
from option import Err, Ok, Result
from PrettyPrinting import bold

# The number of memory entries to show per line when printed
MEMORY_DISPLAY_LENGTH = 4

class Memory():
    
    def __init__(self, capacity: int):
        self.block: list[int] = list(0 for _ in range(0, capacity))
        self.capacity = capacity
        self.size = 0
    
    def __eq__(self, other: Memory):
        
        if not isinstance(other, self.block):
            raise NotImplementedError
        
        return self.block == other.block
    
    def __str__(self) -> str:
        builder: str = ""
        for index in range(0, self.capacity):
            
            if index != 0 and index % MEMORY_DISPLAY_LENGTH == 0:
                builder += "\n"
            
            if index >= self.size: builder += bold(str(self.block[index]))
            else: builder += str(self.block[index])
            
            builder += " "

        return builder
    
    def __getitem__(self, index: int) -> int:
        return self.block[index]
    
    def update(self, value: int, index: int) -> Result[bool, str]:
        if index < 0: return Err("Memory location out of bounds: {} < 0".format(index))
        if index >= self.capacity: return Err("Memory location out of bounds: {} > {}".format(index, self.capacity))
        
        self.block[index] = value
        if index > self.size: self.size = index
        
        return Ok(True)
    
    def update_chunk(self, values: list[int], index: int) -> Result[bool, str]:
        if len(values) == 0: return Err("No values to write!")
        if index < 0: return Err("Memory location out of bounds: {} < 0!".format(index))
        if index >= self.capacity: return Err("Memory location out of bounds: {} > {}!".format(index, self.capacity))
        if index + len(values) >= self.capacity: return Err("Memory location will be out of bounds: {} > {}!".format(index, self.capacity))
        
        self.block[index:index + len(values)] = values
        if index + len(values) > self.size: self.size = index + len(values)

        return Ok(True)
        