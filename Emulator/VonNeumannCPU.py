from __future__ import annotations
from Constants import PC_INC
from Utilities import trace
from Types import Program, Address
from option import Result
from Assembler import Assembler, AssemblerSettings, AssemblerSettingsSource
from PrettyPrinting import PrintMode
from Emulator import CPU

class VonNeumannCPU(CPU):

    def __init__(self):
        pass

    def __eq__(self) -> bool:
        pass

    def __str__(self) -> str:
        pass

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

        r_load = self.memory.load_instructions(program, instruction_base_address, endianness='little')
        if r_load.is_err:
            return trace("failed to load instructions", r_load.unwrap_err())






