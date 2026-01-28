from __future__ import annotations
from option import Ok, Result
from BitManipulation import get_bit, reset_bit, set_bit, toggle_bit
from Constants import CONSTANT_REGISTER_MAP, BP_INC, FL_ZERO, PC_INC, SP_INC, TextRenderTarget
from Utilities import trace

def is_register(reg: str) -> bool:
    return reg in (list(CONSTANT_REGISTER_MAP.keys()) + list(CONSTANT_REGISTER_MAP.values()))

class RegisterFile():
    
    def __init__(self):
        """Creates an empty RegisterFile."""
        
        self.registers = {}
        for r in CONSTANT_REGISTER_MAP.keys():
            self.registers[r] = 0
    
    def __eq__(self, other: RegisterFile):
        
        if not isinstance(other, RegisterFile):
            return NotImplemented
        
        return any(s == o for s, o in zip(self.registers.items(), other.registers.items()))
        
    def __str__(self) -> str:
        """Returns a string representation of a RegisterFile."""

        builder = ""
        for (index, (name, value)) in enumerate(self.registers.items()):
            builder += ("{:2} = {:032b}".format(name, value))
            if index % 4 == 3:
                builder += "\n"
            else:
                builder += " "
        builder += (" " * 143) + "HTIOSPCZ"

        return builder
    
    def to_string(self, target: TextRenderTarget = TextRenderTarget.Terminal):
        """Returns a string representation of a register file
        for either a terminal location or widget rendering."""

        # TODO: TUI: Fix this stuff

        # If this is a terminal render, then just use the str override
        if target == TextRenderTarget.Terminal:
            return str(self)
        
        # If this is a widget render, then split it up a bit
        if target == TextRenderTarget.Widget:
            builder = ""
            for index, (name, value) in enumerate(self.registers.items()):
                builder += " "
                builder += ("{:2} = {:032b}".format(name, value))
                if index % 4 == 3:
                    builder += "\n"
            
            builder += " " * 119 # This sucks
            builder += "    ---- UNUSED ----     HTIOSPCZ\n"
            
            return builder
        
        return f"Invalid TextRenderTarget '{target}'"
    
    def set_reg(self, reg: str, value: int) -> None:
        if reg in self.registers:
            self.registers[reg] = value & 0xFFFFFFFF
    
    def get_reg(self, reg: str) -> Result[int, str]:
        if reg in self.registers:
            return Ok(self.registers[reg])
        return trace(f"No register with key '{reg}'")
    
    def get_pc(self) -> int:
        return self.registers["PC"]
    
    def get_sp(self) -> int:
        return self.registers["SP"]

    def increment_program_counter(self) -> None:
        self.registers['PC'] += PC_INC
    
    def increment_base_pointer(self) -> None:
        self.registers['BP'] += BP_INC
    
    def increment_stack_pointer(self) -> None:
        self.registers['SP'] += SP_INC
    
    def clear_flags(self) -> None:
        self.registers['FL'] = 0
    
    def set_flag(self, flag: int) -> None:
        self.registers['FL'] = set_bit(self.registers['FL'], flag)

    def reset_flag(self, flag: int) -> None:
        self.registers['FL'] = reset_bit(self.registers['FL'], flag)
    
    def get_flag(self, flag: int) -> bool:
        return get_bit(self.registers['FL'], flag)
    
    def toggle_flag(self, flag: int) -> None:
        self.registers['FL'] = toggle_bit(self.registers['FL'], flag)
    
if __name__ == "__main__":
    
    rf = RegisterFile()
    print(rf.to_string(TextRenderTarget.Widget))
    rf.set_flag(FL_ZERO)
    print(rf.to_string(TextRenderTarget.Widget))
    rf.reset_flag(FL_ZERO)
    print(rf.to_string(TextRenderTarget.Widget))
