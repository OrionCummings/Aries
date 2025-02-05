from __future__ import annotations
from option import Ok, Result
from VonNeumannMemory import VonNeumannMemory
from Memory import Memory
from RegisterFile import RegisterFile
from Constants import EC_PC_OVERRUN, PC_INC
from Utilities import trace
from PrettyPrinting import PrintMode
from CPU import CPU, CPUSettings
from Assembler import Assembler, AssemblerSettings, AssemblerSettingsSource

class VonNeumannCPU(CPU):

    def __init__(self, settings: CPUSettings):
        
        super().__init__(settings)

        # Create a register file
        self.register_file = RegisterFile()
        self.register_file.set_reg("PC", self.settings.instruction_memory_base)

        # Create memory boundaries
        instruction_memory_boundary = range(settings.instruction_memory_base, settings.instruction_memory_base + settings.instruction_memory_size)
        data_memory_boundary = range(settings.data_memory_base, settings.data_memory_base + settings.data_memory_size)
        video_memory_boundary = range(settings.video_memory_base, settings.video_memory_base + settings.video_memory_size)
        stack_memory_boundary = range(settings.stack_memory_base, settings.stack_memory_base + settings.stack_memory_size)

        # Create a single memory bank with boundaries
        self.memory = (VonNeumannMemory(self.settings.memory_size)
            .set_instruction_memory_boundary(instruction_memory_boundary)
            .set_data_memory_boundary(data_memory_boundary)
            .set_video_memory_boundary(video_memory_boundary)
            .set_stack_memory_boundary(stack_memory_boundary)
        )

        # Set the highlight range to properly display for memory
        self.memory.set_highlight_range(range(self.settings.instruction_memory_base, self.settings.instruction_memory_base + 4))

    def __eq__(self, other: VonNeumannCPU) -> bool:

        if not isinstance(other, VonNeumannCPU):
            return False
        
        register_file = self.register_file == other.register_file
        memory        = self.memory == other.memory
        
        halt_equal    = self.halted == other.halted

        return (register_file and memory and halt_equal)

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
        if self.memory not in [None, 0] and self.memory.capacity != 0:
            builder += "\nMemory\n"
            builder += str(self.memory)

        return builder

    def get_pc(self) -> int:
        return self.register_file.get_pc()
    
    def get_sp(self) -> int:
        return self.register_file.get_sp()
    
    def set_sp(self, value) -> None:
        self.register_file.set_reg("SP", value)

    def set_highlight_range(self, range) -> None:
        self.memory.set_highlight_range(range)

    def load_program(self, program: Program, program_name: str) -> Result[None, str]:

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

        r_load = self.memory.load_instructions(program, self.settings.instruction_memory_base, endianness='little')
        if r_load.is_err:
            return trace("failed to load instructions", r_load.unwrap_err())
        
        return Ok(None)

    def get_current_instruction(self) -> Result[Instruction, str]:

        r_current_instruction = self.memory.get_instruction(self.register_file.get_pc())
        if r_current_instruction.is_err:
            return trace("failed to get instruction", r_current_instruction.unwrap_err())

        return r_current_instruction
