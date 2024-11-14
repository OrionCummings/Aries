import unittest

from option import Result
from Assembler import Encode, GetOpcode
from RegisterFile import RegisterFile
from Constants import *

def PrintExpectedAndActualBinary(Expected: int, Actual: int):
    print()
    print("Expected: " + format(Expected, "#016b"))
    print("Actual:   " + format(Actual, "#016b"))
    print()

class RegisterFileUnitTests(unittest.TestCase):
    
    def test_GetReg(Self):
        
        # Create a RegisterFile
        R = RegisterFile()
        
        for Reg in REGISTERS.keys():
            R.Registers[Reg] = 4
        
        for Reg in REGISTERS.keys():
            Self.assertEqual(R.GetReg(Reg), 4)
    
    def test_SetReg(Self):
        
        # Create a RegisterFile
        R = RegisterFile()
        
        # Set all registers to
        for Reg in REGISTERS.keys():
            R.SetReg(Reg, 4)
            Self.assertEqual(R.GetReg(Reg), 4)
    
    def test_IncrementInstructionPointer(Self):
        
        # Create a RegisterFile
        R = RegisterFile()
        
        # Increment the instruction pointer
        R.IncrementInstructionPointer()
        
        # Check that the value for the instruction pointer is now 1
        Self.assertEqual(R.Registers['IP'], IP_INC)
    
    def test_IncrementBasePointer(Self):
        
        # Create a RegisterFile
        R = RegisterFile()
        
        # Increment the base pointer
        R.IncrementBasePointer()
        
        # Check that the value for the base pointer is now 1
        Self.assertEqual(R.Registers['BP'], BP_INC)
        
    def test_IncrementStackPointer(Self):
        
        # Create a RegisterFile
        R = RegisterFile()
        
        # Increment the stack pointer
        R.IncrementStackPointer()
        
        # Check that the value for the stack pointer is now 1
        Self.assertEqual(R.Registers['SP'], SP_INC)

    def test_FlagRegisterBitPositions(Self):
        
        # Create a RegisterFile
        R = RegisterFile()
        
        # Ensure the bit position match the documentation
        Self.assertEqual(FL_ZERO, 0)
        Self.assertEqual(FL_CARRY, 1)
        Self.assertEqual(FL_PARITY, 2)
        Self.assertEqual(FL_SIGN, 3)
        Self.assertEqual(FL_OVERFLOW, 4)
        Self.assertEqual(FL_INTERRUPT, 5)
        Self.assertEqual(FL_INTERRUPT_DISABLE, 6)
        Self.assertEqual(FL_TRAP, 7)
        Self.assertEqual(FL_HPC, 8)
    
    def test_ClearFlags(Self):
        
        # Create a RegisterFile
        R = RegisterFile()
        
        # Set the value of the flags register
        R.Registers['FL'] = int(0b0000000111111111)
        
        # Clear the flags register
        R.ClearFlags()
        
        # Check that the value for the flag register is zero
        Self.assertEqual(R.Registers['FL'], 0)
    
    def test_SetFlag(Self):
        
        # Create a RegisterFile
        R = RegisterFile()
        
        # Set all flags
        R.SetFlag(FL_ZERO)
        R.SetFlag(FL_CARRY)
        R.SetFlag(FL_PARITY)
        R.SetFlag(FL_SIGN)
        R.SetFlag(FL_OVERFLOW)
        R.SetFlag(FL_INTERRUPT)
        R.SetFlag(FL_INTERRUPT_DISABLE)
        R.SetFlag(FL_TRAP)
        R.SetFlag(FL_HPC)
        
        # Check that the value for the flag register is zero
        Self.assertEqual(R.Registers['FL'], int(0b0000000111111111))

    def test_GetFlag(Self):
        
        # Create a RegisterFile
        R = RegisterFile()
        
        # Set the flags register
        R.Registers['FL'] = int(0b0000000101010101)
        
        # Get all flags
        ZeroValue = R.GetFlag(FL_ZERO)
        CarryValue = R.GetFlag(FL_CARRY)
        ParityValue = R.GetFlag(FL_PARITY)
        SignValue = R.GetFlag(FL_SIGN)
        OverflowValue = R.GetFlag(FL_OVERFLOW)
        InterruptValue = R.GetFlag(FL_INTERRUPT)
        InterruptDisableValue = R.GetFlag(FL_INTERRUPT_DISABLE)
        TrapValue = R.GetFlag(FL_TRAP)
        HPCValue = R.GetFlag(FL_HPC)
        
        # Check that the values match
        Self.assertEqual(ZeroValue, 1)
        Self.assertEqual(CarryValue, 0)
        Self.assertEqual(ParityValue, 1)
        Self.assertEqual(SignValue, 0)
        Self.assertEqual(OverflowValue, 1)
        Self.assertEqual(InterruptValue, 0)
        Self.assertEqual(InterruptDisableValue, 1)
        Self.assertEqual(TrapValue, 0)
        Self.assertEqual(HPCValue, 1)

    def test_ToggleFlag(Self):
        
        # Create a RegisterFile
        R = RegisterFile()

        # Set the flags register
        R.Registers['FL'] = int(0b0000000101010101)
        
        # Toggle all flags
        R.ToggleFlag(FL_ZERO)
        R.ToggleFlag(FL_CARRY)
        R.ToggleFlag(FL_PARITY)
        R.ToggleFlag(FL_SIGN)
        R.ToggleFlag(FL_OVERFLOW)
        R.ToggleFlag(FL_INTERRUPT)
        R.ToggleFlag(FL_INTERRUPT_DISABLE)
        R.ToggleFlag(FL_TRAP)
        R.ToggleFlag(FL_HPC)
        
        # Check that the value for the flag register is zero
        Self.assertEqual(R.Registers['FL'], int(0b0000000010101010))

class ALUUnitTests(unittest.TestCase):
    
    @unittest.skip("Not implemented")
    def test_NOP(Self):
        Self.fail()
    
    @unittest.skip("Not implemented")
    def test_ADD(Self):
        Self.fail()
        
    @unittest.skip("Not implemented")
    def test_SUB(Self):
        Self.fail()
        
    @unittest.skip("Not implemented")
    def test_AND(Self):
        Self.fail()
        
    @unittest.skip("Not implemented")
    def test_OR(Self):
        Self.fail()
        
    @unittest.skip("Not implemented")
    def test_NOT(Self):
        Self.fail()
        
    @unittest.skip("Not implemented")
    def test_SHR(Self):
        Self.fail()
        
    @unittest.skip("Not implemented")
    def test_SHL(Self):
        Self.fail()
    
class InstructionMemoryUnitTests(unittest.TestCase):
    pass

class DataMemoryUnitTests(unittest.TestCase):
    pass

class ProgramCounterUnitTests(unittest.TestCase):
    pass

class AssemblerFunctionUnitTests(unittest.TestCase):
    
    def OpcodeComparison(Self, Expected: int, Line: str):
        RActual = GetOpcode(Line)
        Actual = RActual.unwrap_or_else(lambda: Self.fail("Failed to parse opcode"))
        Self.assertEqual(Expected, Actual)
        
    def test_GetOpcodeNOP(Self):
        Line = 'nop'
        Expected = OPCODES['nop']
        Self.OpcodeComparison(Expected, Line)
        
    def test_GetOpcodeHLT(Self):
        Line = 'hlt'
        Expected = OPCODES['hlt']
        Self.OpcodeComparison(Expected, Line)

    def test_GetOpcodeADD(Self):
        Line = 'add A B C'
        Expected = OPCODES['add']
        Self.OpcodeComparison(Expected, Line)
        
    def test_GetOpcodeADDI(Self):
        Line = 'addi A B 28921'
        Expected = OPCODES['addi']
        Self.OpcodeComparison(Expected, Line)

    @unittest.skip("Unimplemented")
    def test_GetArg1(Self):
        pass
    
    @unittest.skip("Unimplemented")
    def test_GetArg2(Self):
        pass
    
    @unittest.skip("Unimplemented")
    def test_GetArg3(Self):
        pass

class AssemblerUnitTests(unittest.TestCase):
    
    def test_Encode_NOP(Self):
        Line = 'nop'
                   # XXXXXX_XXXX_XXXX_XX_XXXXXXXXXXXXXXXX
        Expected = 0b000000_0000_0000_00_0000000000000000
        RActual: Result = Encode(Line)
        if RActual.is_err:
            Self.fail("Failed to encode: {}".format(RActual.unwrap_err))
        Self.assertEqual(Expected, RActual.unwrap())
        
    def test_Encode_HLT(Self):
        Line = 'hlt'
                   # XXXXXX_XXXX_XXXX_XX_XXXXXXXXXXXXXXXX
        Expected = 0b000001_0000_0000_0000_00000_000000000
        RActual: Result = Encode(Line)
        if RActual.is_err:
            Self.fail("Failed to encode: {}".format(RActual.unwrap_err))
        Self.assertEqual(Expected, RActual.unwrap())

    def test_Encode_LDI_Hex(Self):
        Line = 'ldi A 0xFFFF'
        Vec = Line.split(' ')
                   # XXXXXX_XXXX_XXXXXX_XXXXXXXXXXXXXXXX
        Expected = 0b001111_0000_000000_1111111111111111
        RActual: Result = Encode(*Vec)
        if RActual.is_err:
            Self.fail("Failed to encode: {}".format(RActual.unwrap_err()))
        Self.assertEqual(Expected, RActual.unwrap())

    def test_Encode_LDI_Octal(Self):
        Line = 'ldi B 0o1720'
        Vec = Line.split(' ')
                   # XXXXXX_XXXX_XXXXXX_XXXXXXXXXXXXXXXX
        Expected = 0b001111_0001_000000_0000001111010000
        RActual: Result = Encode(*Vec)
        if RActual.is_err:
            Self.fail("Failed to encode: {}".format(RActual.unwrap_err()))
        Self.assertEqual(Expected, RActual.unwrap())
        
    def test_Encode_LDI_Binary(Self):
        Line = 'ldi C 0b1101010111010010'
        Vec = Line.split(' ')
                   # XXXXXX_XXXX_XXXXXX_XXXXXXXXXXXXXXXX
        Expected = 0b001111_0010_000000_1101010111010010
        RActual: Result = Encode(*Vec)
        if RActual.is_err:
            Self.fail("Failed to encode: {}".format(RActual.unwrap_err()))
        Self.assertEqual(Expected, RActual.unwrap())
        
    def test_Encode_LDI_Decimal(Self):
        Line = 'ldi G 16726'
        Vec = Line.split(' ')
                   # XXXXXX_XXXX_XXXXXX_XXXXXXXXXXXXXXXX
        Expected = 0b001111_0110_000000_0100000101010110
        RActual: Result = Encode(*Vec)
        if RActual.is_err:
            Self.fail("Failed to encode: {}".format(RActual.unwrap_err()))
        
        Self.assertEqual(Expected, RActual.unwrap())

if __name__ == '__main__':
    unittest.main(verbosity=2)