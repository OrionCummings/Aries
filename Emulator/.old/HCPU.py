from __future__ import annotations
from option import Err, Ok, Result
from CPU import CPUSettings
from Cache import Cache
from ALU import ALU
from FPU import FPU
from RegisterFile import RegisterFile
from Transformations import decode

class HCPU():

    def __init__(self, settings: CPUSettings):

        # Create a RegisterFile
        self.register_file = RegisterFile()

        # Create a Cache
        self.cache = Cache()

        # Create an ALU
        self.alu = ALU()

        # Create an FPU
        self.fpu = FPU()

    def __eq__(self, other: HCPU) -> bool:

        if not isinstance(other, HCPU):
            return False
        
        register_file_equal = self.register_file == other.register_file
        cache_equal         = self.cache == other.cache
        alu_equal           = self.alu == other.alu
        fpu_equal           = self.fpu == other.fpu
        halt_equal          = self.halted == other.halted
        
        return (register_file_equal and cache_equal and alu_equal and fpu_equal and halt_equal)

    def __str__(self) -> str:

        # Get the program counter
        program_counter = self.register_file.get_pc()
        
        # Begin the string builder by including the program counter
        builder: str = "PC: " + str(program_counter) + "\n"

        # Append the register file
        builder += "Register File\n"
        builder += str(self.register_file)

        # Append the cache
        # builder += "\nCache\n"
        # builder += str(self.cache)

        # Append the ALU
        # builder += "\nALU\n"
        # builder += str(self.alu)

        # Append the FPU
        # builder += "\nFPU\n"
        # builder += str(self.fpu)
        
        return builder

    def get_pc(self) -> int:
        return self.register_file.get_pc()
    
    def get_sp(self) -> int:
        return self.register_file.get_sp()
    
    def set_sp(self, value) -> int:
        return self.register_file.set_reg("SP", value)
    