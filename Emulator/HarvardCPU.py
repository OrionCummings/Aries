from __future__ import annotations
import struct
from enum import Enum
from option import Err, Ok, Result
from CPU import CPU, CPUSettings
from Types import Program, Address, Instruction
from Assembler import Assembler, AssemblerSettings, AssemblerSettingsSource
from Stack import Stack
from Memory import Memory
from RegisterFile import RegisterFile
from Transformations import decode
from PrettyPrinting import PrintMode, green_bold, info, warning
from Utilities import abc_not_implemented, panic, debug, trace
from Constants import CONSTANT_REGISTER_MAP, DEFAULT_DATA_MEMORY_BASE_ADDRESS, DEFAULT_DATA_MEMORY_SIZE_IN_BYTES, DEFAULT_INSTRUCTION_MEMORY_BASE_ADDRESS, DEFAULT_INSTRUCTION_MEMORY_SIZE_IN_BYTES, DEFAULT_STACK_MEMORY_BASE_ADDRESS, DEFAULT_STACK_MEMORY_SIZE_IN_BYTES, DEFAULT_VIDEO_MEMORY_BASE_ADDRESS, DEFAULT_VIDEO_MEMORY_SIZE_IN_BYTES, FL_ZERO, PC_INC, EC_PC_OVERRUN, TextRenderTarget

class HarvardCPU(CPU):

    def __init__(self, settings: CPUSettings):

        super().__init__(settings)

        # Create a register file
        self.register_file = RegisterFile()

        # Create seperate memory banks for each type of memory
        self.instruction_memory = Memory(self.settings.instruction_memory_size)
        self.data_memory = Memory(self.settings.data_memory_size)
        self.video_memory = Memory(self.settings.video_memory_size)
        self.stack_memory = Stack(self.settings.stack_memory_size)

        # Set the highlight range to properly display for instruction memory
        self.instruction_memory.set_highlight_range(range(0, 4))

    def __eq__(self, other: CPU) -> bool:

        if not isinstance(other, CPU):
            return NotImplemented
        
        register_file_equal        = self.register_file == other.register_file
        instruction_memory_equal   = self.instruction_memory == other.instruction_memory
        data_memory_equal          = self.data_memory == other.data_memory
        stack                      = self.stack_memory == other.stack_memory
        
        halt_equal                 = self.halted == other.halted
        
        return (register_file_equal and instruction_memory_equal and data_memory_equal and stack and halt_equal)

    def __str__(self) -> str:

        # Get the program counter
        program_counter = self.register_file.get_pc()
        
        # Begin the string builder by including the program counter
        builder: str = "PC: " + str(program_counter) + "\n"

        # Append the register file if it exists
        if self.register_file not in [None, 0]:
            builder += "Register File\n"
            builder += str(self.register_file)

        # Append the instruction memory if it exists
        if self.instruction_memory not in [None, 0] and self.instruction_memory.capacity != 0:
            builder += "\nInstruction Memory\n"
            builder += str(self.instruction_memory)

        # Append the data memory if it exists
        if self.data_memory not in [None, 0] and self.data_memory.capacity != 0:
            builder += "\n\nData Memory\n"
            builder += str(self.data_memory)

        # Append the video memory if it exists
        if self.video_memory not in [None, 0] and self.video_memory.capacity != 0:
            builder += "\n\nVideo Memory\n"
            builder += str(self.video_memory)

        # Append the stack if it exists
        if self.stack_memory not in [None, 0] and self.stack_memory.capacity != 0:
            builder += "\n\nStack\n"
            builder += str(self.stack_memory)
        
        return builder

    def load_program(self, program: Program, program_name: str, instruction_base_address: Address = 0) -> Result[None, str]:

        # If the input is a string, then assemble that string and reassign `program`
        if isinstance(program, str):

            assmbler_settings = (AssemblerSettings()
                .set_file_name(program_name)
                .set_print_mode(PrintMode.NoOutput)
                .set_source(AssemblerSettingsSource.String)
            )

            assembler = Assembler(assmbler_settings)

            r_run = assembler.run(program)
            if r_run.is_err:
                return trace("failed to run assembler", r_run.unwrap_err())

            program = assembler.instructions

        # If the instruction base address is higher than the instruction memory capacity,
        # then there is no way for this program to be loaded successfully; error
        if instruction_base_address > self.instruction_memory.capacity:
            return trace("program begins outside of memory address space")
        
        # If the length of the program overruns the instruction memory capacity,
        # then there is no way for this program to be loaded successfully; error
        program_length_in_bytes = len(program) * PC_INC
        if program_length_in_bytes + instruction_base_address > self.instruction_memory.capacity:
            return trace(f"program size ({program_length_in_bytes}) exceeds the instruction memory capacity ({self.instruction_memory.capacity})!")
        
        # If the program is empty, this is probably an issue
        if program_length_in_bytes == 0: warning("loading null program")
        
        # Load the instructions into instruction memory starting at the instruction base address
        r_update = self.instruction_memory.load_instructions(program, instruction_base_address)
        if r_update.is_err: return trace("failed to load instructions", r_update.unwrap_err())

        info(f"Loaded '{program_name}' starting at address {instruction_base_address} ({instruction_base_address:0X})")

        return Ok(None)

    def get_current_instruction(self) -> Result[Instruction, str]:

        r_current_instruction = self.instruction_memory.get_instruction(self.register_file.get_pc())
        if r_current_instruction.is_err:
            return trace("failed to get instruction", r_current_instruction.unwrap_err())

        return r_current_instruction






