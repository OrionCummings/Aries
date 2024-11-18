
from option import Result, Err, Ok
from Assembler import GetOpcode
from Constants import OPCODES

def VerifyOpcode(Instruction: int, ExpectedOpcode: str) -> Result[bool, str]:
    ROpcode = GetOpcode(Instruction)
    if ROpcode.is_err: return Err(ROpcode.unwrap_err())
    ActualOpcode = ROpcode.unwrap()
    if not ActualOpcode == OPCODES[ExpectedOpcode][0]:
        return Err("Expected opcode '{}' does not match actual opcode '{}' from instruction {}".format(ExpectedOpcode, ActualOpcode, Instruction))
    return True
    
def InsNOP(Instruction: int) -> Result[bool, str]:
    """Executes a 'nop' instruction."""
    
    RVerification = VerifyOpcode(Instruction, 'nop')
    if RVerification.is_err: return Err(RVerification.unwrap_err())

    return Ok(True)