from __future__ import annotations
from enum import Enum
from option import Err, Ok, Result
from Constants import TextRenderTarget
from PrettyPrinting import bold

# The number of memory entries to show per line when printed
TERMINAL_MEMORY_DISPLAY_LENGTH = 16
WIDGET_MEMORY_DISPLAY_LENGTH = 16

# TODO: Fix this class
# There a many assumptions about the layout/alignment of memory
# that are not documented nor consistent!
# * Should memory be bit-addressable?
# * How is (1 byte) memory alignment being enforced?
# * How should numbers larger than a single byte be handled?
# * How should negative numbers be handled? -This one is more complex, and should be addressed last!
class Memory():
    """A byte-addressable block of memory designed to simulate either data or instruction memory.
    """
    
    def __init__(self, capacity: int):
        """Creates an empty Memory class. Initializes all memory to zero.

        Args:
            capacity (int): The size of memory. Expected (but not required) to be a power of 2.
        """
        
        self.bytes = bytearray(capacity)
        self.capacity = capacity
    
    def __eq__(self, other: Memory) -> bool:
        """Equality operator overload. Determines if two Memory instances are equivalent.

        Args:
            other (Memory): The other Memory instance.

        Raises:
            NotImplementedError: An error to show that equality between a Memory instance and anything that is not a
            Memory instance is not a defined operation.

        Returns:
            bool: Returns boolean True if both Memory instances are equivalent.
        """
        
        if not isinstance(other, self.bytes):
            raise NotImplementedError
        
        return self.bytes == other.bytes
    
    def __str__(self) -> str:
        """Converts a Memory instance into a string representation. Ideal for printing.

        Returns:
            str: A string representation of the Memory instance.
        """
        
        builder: str = ""
        for index in range(0, self.capacity):
            
            if index != 0 and index % TERMINAL_MEMORY_DISPLAY_LENGTH == 0:
                builder += "\n"
            
            builder += "{:02X}".format(self.bytes[index])
            builder += " "

        return builder
    
    def to_string(self, target: TextRenderTarget = TextRenderTarget.Terminal) -> str:
        """A function to convert a Memory instance into a string, similar to the string overload. Accepts an additional
        parameter to determine the target display.

        Args:
            target (TextRenderTarget, optional): The target render location. Defaults to TextRenderTarget.Terminal.

        Returns:
            str: A string representation of a Memory instance that is suitable for the given render target.
        """
        
        if target == TextRenderTarget.Terminal:
            return str(self)
        
        if target == TextRenderTarget.Widget:
            builder: str = ""
            for index in range(0, self.capacity):
                
                if index != 0 and index % WIDGET_MEMORY_DISPLAY_LENGTH == 0:
                    builder += "\n"
                
                builder += "{:02X}".format(self.bytes[index])
                builder += " "

            return builder
    
    def get_bytes(self, start_index: int, end_index: int) -> Result[bytes, str]:
        """Gets the bytes between the given indices.

        Args:
            start_index (int): The start index of the desired range.
            end_index (int): The end index of the desired range.

        Returns:
            Result[bytes, str]: A boolean True on success or a error message string on failure.
        """
        
        if start_index > end_index: return Err(f"Start index {start_index} > end index {end_index}!")
        if start_index < 0 or start_index > self.capacity: return Err(f"Start index {start_index} out of range!")
        if end_index   < 0 or   end_index > self.capacity: return Err(f"End index {end_index} out of range!")
        return Ok(self.bytes[start_index, end_index])
    
    def set_bytes(self, values: bytearray, indices: list[int] | range) -> Result[bool, str]:
        """Sets the contents of memory based on the passed values and types.

        Args:
            values (bytearray): An array of bytes to be written to memory
            indices (list[int] | range): Either a list of indices corresponding to each values passed as `values` or 
            a contiguous range of indices. If this is of type `range`, then the `values` array is expected to contain 
            a single element that will be written to all memory addresses as specified by `indices`

        Returns:
            Result[bool, str]: A result type containing a boolean True on success or a string error message on failure.
        """
        
        if len(values) == 0: return Err("No values to write!")
        if len(values) != len(indices) and len(values) == 1:
            values = values * len(indices)
        
        if isinstance(indices, range):
            indices = list(indices)
        
        for (i, index) in enumerate(indices):
            if index < 0: return Err("Memory location out of bounds: {} < 0!".format(index))
            if index >= self.capacity: return Err("Memory location out of bounds: {} > {}!".format(index, self.capacity))
            self.bytes[index] = values[i]

        return Ok(True)
    
    def load_instruction(self, instruction: int, index: int, endianness: str = 'little') -> Result[bool, str]:
        """Loads the given instruction into the Memory instance in the specified endian order and beginning at the start
        index. All instructions are 32-bit, so this function will update `index` and the following three indices after `index`.

        Args:
            instruction (int): The instruction to be loaded into this Memory instance.
            index (int): The index to start loading the instruction.
            endianness (int): A string that determines endianness. Can only be 'little' or 'big'. Defaults to 'little'.

        Returns:
            Result[bool, str]: A result type containing a boolean True on success or a string error message on failure.
        """

        if instruction > 2**32: return Err(f"Invalid instruction '{instruction}': too large!")
        if instruction < 0: return Err(f"Invalid instruction '{instruction}': too small!")
        if endianness not in ['little', 'big']: return Err(f"Invalid endianness '{endianness}'!")
        if len(self.bytes) < index: return Err(f"Memory location '{index}' out of bounds!")
        
        deconstructed_instruction = instruction.to_bytes(4, endianness)
        set_bytes_result = self.set_bytes(deconstructed_instruction, list(range(index, index + len(deconstructed_instruction))))
        if set_bytes_result.is_err: return Err(set_bytes_result.Err())
        
        return Ok(True)
    
    def load_instructions(self, instructions: list[int], index: int, endianness: str = 'little') -> Result[bool, str]:
        
        for (i, instruction) in enumerate(instructions):
            load_result = self.load_instruction(instruction, index + (i * 4), endianness)
            if load_result.is_err: return Err(load_result.Err())
        
        return Ok(True)

if __name__ == "__main__":
    
    memory = Memory(128)
    r = memory.set_bytes(bytearray([255]), range(0, 4))
    
    i1 = [0b11111111_11111111_00000000_00000000] * 8
    i2 = [0b11001100_00001111_00001111_00001010] * 8
    instructions = [val for pair in zip(i1, i2) for val in pair]
    memory.load_instructions(instructions, 16)
    
    print("Terminal")
    print(memory.to_string(TextRenderTarget.Terminal))
    print()
    print("Widget")
    print(memory.to_string(TextRenderTarget.Widget))
    