from __future__ import annotations
from option import Err, Ok, Result

from Constants import register_map, BP_INC, PC_INC, SP_INC, set_bit, get_bit, toggle_bit

class RegisterFile():
    
    def __init__(self):
        """Creates an empty RegisterFile."""
        
        self.registers = {}
        for r in register_map.keys():
            self.registers[r] = 0
    
    def __eq__(self, other: RegisterFile):
        
        if not isinstance(other, RegisterFile):
            return NotImplemented
        
        for s, o in zip(self.registers.items(), other.registers.items()):
            if s != o: return False
            
        return True
        
    def __str__(self) -> str:
        """Returns a string representation of a RegisterFile."""

        builder = ""
        for r in self.registers.items():
            builder += ("{:2} = {:032b}".format(r[0], r[1]))
            builder += "\n"
        builder += "                             HTIOSPCZ"

        return builder
    
    def set_reg(self, reg: str, value: int) -> None:
        if reg in self.registers:
            self.registers[reg] = value & 0xFFFFFFFF
    
    def get_reg(self, reg: str) -> Result[int, str]:
        if reg in self.registers:
            return Ok(self.registers[reg])
        return Err("No register with key '{}'!".format(reg))
    
    def get_pc(self) -> int:
        return self.registers["PC"]
    
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
    
    def get_flag(self, flag: int) -> bool:
        return get_bit(self.registers['FL'], flag)
    
    def toggle_flag(self, flag: int) -> None:
        self.registers['FL'] = toggle_bit(self.registers['FL'], flag)
    
if __name__ == "__main__":
    
    rf = RegisterFile()
    print(rf)
    print()
    
    rf.set_reg("B", 255)
    rf.set_reg("G", 16000)
    rf.set_reg("H", 2367471)
    print(rf)
    
    print(rf.get_reg("A").unwrap())
    print(rf.get_reg("B").unwrap())
    print(rf.get_reg("G").unwrap())
    print(rf.get_reg("H").unwrap())
    
    