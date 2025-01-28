from __future__ import annotations
from enum import Enum
from option import Err, Ok, Result
from ByteBank import ByteBank
from Constants import PC_INC, TextRenderTarget
from PrettyPrinting import bold, red_bold
from Utilities import trace

# The number of memory entries to show per line when printed
TERMINAL_MEMORY_DISPLAY_LENGTH = 16
WIDGET_MEMORY_DISPLAY_LENGTH = 16

class Memory(ByteBank):
    """A byte-addressable block of memory.
    """
    
    def __init__(self, capacity_in_bytes: int):
        """Creates an empty Memory class. Initializes all memory to zero.

        Args:
            capacity (int): The size of memory in bytes. Expected (but not required) to be a power of 2.
        """
        super().__init__(capacity_in_bytes)
    
    def __eq__(self, other: Memory) -> bool:
        """Equality operator overload. Determines if two Memory instances are equivalent.

        Args:
            other (Memory): The other Memory instance.

        Returns:
            bool: Returns boolean True if both Memory instances are equivalent.
        """

        return \
            (self.capacity, self.content) == (other.capacity, other.content)
    
    def __str__(self) -> str:
        """Converts a Memory instance into a string representation. Ideal for printing.

        Returns:
            str: A string representation of the Memory instance.
        """

        return super().__str__()
       
    def get_instruction(self, index: int) -> Result[int, str]:
        
        if index not in range(0, self.capacity): return trace(f"index '{index}' out of range")
        if index % 4 != 0: return trace(f"index '{index}' is not aligned with four byte boundary")

        r = list(range(index, index + 4))

        r_get_bytes = self.get_bytes(r)
        if r_get_bytes.is_err:
            return trace("failed to get bytes", r_get_bytes.unwrap_err())
        
        instruction = int.from_bytes(r_get_bytes.unwrap(), byteorder='little')

        return Ok(instruction)

    def load_instruction(self, instruction: int, index_in_bytes: int, endianness: str = 'little') -> Result[bool, str]:
        """Loads the given instruction into the Memory instance in the specified endian order and beginning at the start
        index. All instructions are 32-bit, so this function will update `index` and the following three indices after `index`.

        Args:
            instruction (int): The instruction to be loaded into this Memory instance.
            index (int): The index to start loading the instruction.
            endianness (int): A string that determines endianness. Can only be 'little' or 'big'. Defaults to 'little'.

        Returns:
            Result[bool, str]: A result type containing a boolean True on success or a string error message on failure.
        """

        if instruction > 2**32: return trace(f"Invalid instruction '{instruction}': too large!")
        if instruction < 0: return trace(f"Invalid instruction '{instruction}': too small!")
        if endianness not in ['little', 'big']: return trace(f"Invalid endianness '{endianness}'!")
        if len(self.content) < index_in_bytes: return trace(f"Memory location '{index_in_bytes}' out of bounds!")
        
        instruction_as_bytes = instruction.to_bytes(4, endianness)
        r_set_bytes = self.set_bytes(range(index_in_bytes, index_in_bytes + PC_INC), instruction_as_bytes)
        if r_set_bytes.is_err: return trace("failed to set bytes", r_set_bytes.unwrap_err())
        
        return Ok(True)
    
    def load_instructions(self, instructions: list[int], index: int, endianness: str = 'little') -> Result[bool, str]:
        
        for (i, instruction) in enumerate(instructions):
            load_result = self.load_instruction(instruction, index + (i * 4), endianness)
            if load_result.is_err: return trace("failed to load instruction", load_result.unwrap_err())
        
        return Ok(True)

