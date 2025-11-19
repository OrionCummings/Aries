from __future__ import annotations
from Memory import Memory
from Types import Instruction
from enum import Enum
from option import Err, Ok, Result
from ByteBank import ByteBank
from Constants import HEX_FORMAT, PC_INC, TextRenderTarget
from PrettyPrinting import blue, bold, green, orange, red, red_bold, yellow
from Utilities import trace

class VonNeumannMemory(Memory):
    """A byte-addressable block of memory.
    """
    
    def __init__(self, capacity_in_bytes: int):
        super().__init__(capacity_in_bytes)

        # Initialize memory boundaries
        self.instruction_memory_boundary = None
        self.data_memory_boundary = None
        self.video_memory_boundary = None
        self.stack_memory_boundary = None
    
    def __eq__(self, other: VonNeumannMemory) -> bool:
        return isinstance(other, Memory) and \
            (self.capacity, self.content) == (other.capacity, other.content)
    
    def __str__(self) -> str:

        # Create the string builder
        builder = ""

        # For every byte in memory, ...
        for index in range(0, self.capacity):

            if index % self.print_num_rows == 0:
                builder += f"0x{index:08X} "

            # Color each section in memory
            if index in self.instruction_memory_boundary:

                # If the current address in memory is in the highlight range, print it in bold
                if self.highlight_range is not None and index in self.highlight_range:
                    builder += red_bold(HEX_FORMAT.format(self.content[index]))
                else:
                    builder += red(HEX_FORMAT.format(self.content[index]))

            elif index in self.data_memory_boundary:
                builder += blue(HEX_FORMAT.format(self.content[index]))

            elif index in self.video_memory_boundary:
                builder += yellow(HEX_FORMAT.format(self.content[index]))

            elif index in self.stack_memory_boundary:
                builder += green(HEX_FORMAT.format(self.content[index]))

            else:
                builder += HEX_FORMAT.format(self.content[index])

            # Add a space between bytes
            builder += " "

            # If the index is at the end of the line, ...
            if index % self.print_num_rows == self.print_num_rows - 1:

                # Add the bytes in this line as text
                for line_index in range(index - self.print_num_rows, index):
                    byt: int = self.content[line_index]
                    if byt == 0:
                        string = '0'
                    else:
                        string = chr(byt)
                    builder += string

                # Add a new line
                builder += '\n'

        return builder

    def get_instruction(self, index: int) -> Result[Instruction, str]:
        
        if index not in range(0, self.capacity): return trace(f"index '{index}' out of range")
        if index % 4 != 0: return trace(f"index '{index}' is not aligned with four byte boundary")

        r = list(range(index, index + 4))

        r_get_bytes = self.get_bytes(r)
        if r_get_bytes.is_err:
            return trace("failed to get bytes", r_get_bytes.unwrap_err())
        
        instruction: Instruction = int.from_bytes(r_get_bytes.unwrap(), byteorder='little')

        return Ok(instruction)

    def load_instruction(self, instruction: int, index_in_bytes: int, endianness: str = 'little') -> Result[None, str]:

        if instruction > 2**32: return trace(f"Invalid instruction '{instruction}': too large!")
        if instruction < 0: return trace(f"Invalid instruction '{instruction}': too small!")
        if endianness not in ['little', 'big']: return trace(f"Invalid endianness '{endianness}'!")
        if len(self.content) < index_in_bytes: return trace(f"Memory location '{index_in_bytes}' out of bounds!")
        
        instruction_as_bytes = instruction.to_bytes(4, endianness)
        r_set_bytes = self.set_bytes(range(index_in_bytes, index_in_bytes + PC_INC), instruction_as_bytes)
        if r_set_bytes.is_err: return trace("failed to set bytes", r_set_bytes.unwrap_err())
        
        return Ok(None)
    
    def load_instructions(self, instructions: list[int], index: int, endianness: str = 'little') -> Result[None, str]:
        
        for (i, instruction) in enumerate(instructions):
            load_result = self.load_instruction(instruction, index + (i * 4), endianness)
            if load_result.is_err: return trace("failed to load instruction", load_result.unwrap_err())
        
        return Ok(None)

    def set_instruction_memory_boundary(self, boundary: range) -> Memory:
        self.instruction_memory_boundary = boundary
        return self

    def set_data_memory_boundary(self, boundary: range) -> Memory:
        self.data_memory_boundary = boundary
        return self

    def set_video_memory_boundary(self, boundary: range) -> Memory:
        self.video_memory_boundary = boundary
        return self

    def set_stack_memory_boundary(self, boundary: range) -> Memory:
        self.stack_memory_boundary = boundary
        return self

