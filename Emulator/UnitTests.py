import unittest

from option import Result
from Instructions import ADD, NOP, Encode, GetOpcode
from Memory import Memory
from RegisterFile import RegisterFile
from CPU import CPU
from Constants import *

def PrintExpectedAndActualBinary(Expected: int, Actual: int):
    print()
    print("Expected: " + format(Expected, "032b"))
    print("Actual:   " + format(Actual, "032b"))
    print()

class RegisterFileUnitTests(unittest.TestCase):
    
    def test_RegisterFileEquality(Self):
        
        RegisterFileA: RegisterFile = RegisterFile()
        RegisterFileB: RegisterFile = RegisterFile()
        
        # TODO: Make this test more robust; this doesn't test much at all
        Self.assertTrue(RegisterFileA == RegisterFileB)
    
    def test_GetReg(Self):
        
        # Create a RegisterFile
        R = RegisterFile()
        
        for Reg in REGISTERS.keys():
            R.Registers[Reg] = 4
        
        for Reg in REGISTERS.keys():
            RValue = R.GetReg(Reg)
            if RValue.is_err: Self.fail(RValue.Err)
            Value = RValue.unwrap()
            Self.assertEqual(Value, 4)
    
    def test_SetReg(Self):
        
        # Create a RegisterFile
        R = RegisterFile()
        
        # Set all registers to
        for Reg in REGISTERS.keys():
            R.SetReg(Reg, 4)
            
            RValue = R.GetReg(Reg)
            if RValue.is_err: Self.fail(RValue.Err)
            Value = RValue.unwrap()
            Self.assertEqual(Value, 4)
    
    def test_IncrementProgramCounter(Self):
        
        # Create a RegisterFile
        R = RegisterFile()
        
        # Increment the instruction pointer
        R.IncrementProgramCounter()
        
        # Check that the value for the instruction pointer is now 1
        Self.assertEqual(R.Registers['PC'], PC_INC)
    
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
        Self.assertEqual(FL_TRAP, 6)
        Self.assertEqual(FL_HPC, 7)
    
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
        R.SetFlag(FL_TRAP)
        R.SetFlag(FL_HPC)
        
        # Check that the value for the flag register is zero
        Self.assertEqual(R.Registers['FL'], int(0b0000000011111111))

    def test_GetFlag(Self):
        
        # Create a RegisterFile
        R = RegisterFile()
        
        # Set the flags register
        R.Registers['FL'] = int(0x000000FF)
        
        # Get all flags
        ZeroValue = R.GetFlag(FL_ZERO)
        CarryValue = R.GetFlag(FL_CARRY)
        ParityValue = R.GetFlag(FL_PARITY)
        SignValue = R.GetFlag(FL_SIGN)
        OverflowValue = R.GetFlag(FL_OVERFLOW)
        InterruptValue = R.GetFlag(FL_INTERRUPT)
        TrapValue = R.GetFlag(FL_TRAP)
        HPCValue = R.GetFlag(FL_HPC)
        
        # Check that the values match
        Self.assertEqual(ZeroValue, 1)
        Self.assertEqual(CarryValue, 1)
        Self.assertEqual(ParityValue, 1)
        Self.assertEqual(SignValue, 1)
        Self.assertEqual(OverflowValue, 1)
        Self.assertEqual(InterruptValue, 1)
        Self.assertEqual(TrapValue, 1)
        Self.assertEqual(HPCValue, 1)

    def test_ToggleFlag(Self):
        
        # Create a RegisterFile
        R = RegisterFile()

        # Set the flags register
        R.Registers['FL'] = int(0x000000FF)
        
        # Toggle all flags
        R.ToggleFlag(FL_ZERO)
        R.ToggleFlag(FL_CARRY)
        R.ToggleFlag(FL_PARITY)
        R.ToggleFlag(FL_SIGN)
        R.ToggleFlag(FL_OVERFLOW)
        R.ToggleFlag(FL_INTERRUPT)
        R.ToggleFlag(FL_TRAP)
        R.ToggleFlag(FL_HPC)
        
        # Check that the value for the flag register is zero
        Self.assertEqual(R.Registers['FL'], int(0x00000000))

class CPUUnitTests(unittest.TestCase):
    
    def test_CPUEquality(Self):
        
        CPUA: CPU = CPU(16, 16)
        CPUB: CPU = CPU(16, 16)
        
        # TODO: Make this test more robust; this doesn't test much at all
        Self.assertTrue(CPUA == CPUB)

class InstructionUnitTests(unittest.TestCase):
    
    def test_NOP(Self):
        OriginalCPU: CPU = CPU(16, 16)
        ExpectedCPU: CPU = CPU(16, 16)
        
        Line = 'nop'
        RInstruction = Encode(Line)
        if RInstruction.is_err: Self.fail(RInstruction.Err())
        Instruction = RInstruction.unwrap()
        
        RActualCPU = NOP(OriginalCPU, Instruction)
        if RActualCPU.is_err: Self.fail(RActualCPU.Err())
        ActualCPU = RActualCPU.unwrap()
        
        Self.assertTrue(ExpectedCPU == ActualCPU)
    
    def test_ADD(Self):
        
        
        # NOTE: These tests aren't amazing and they actually could use
        # opcode information from the Encode() call.
        
        OriginalCPU: CPU = CPU(16, 16)
        
        ExpectedCPU: CPU = CPU(16, 16)
        ExpectedCPU.RegisterFile.Registers['A'] = 4
        ExpectedCPU.RegisterFile.Registers['B'] = 3
        ExpectedCPU.RegisterFile.Registers['C'] = 7
        
        Line = 'add A B C'
        RInstruction = Encode(Line)
        if RInstruction.is_err: Self.fail(RInstruction.unwrap_err())
        Instruction = RInstruction.unwrap()
        
        RActualCPU = ADD(OriginalCPU, Instruction)
        if RActualCPU.is_err: Self.fail(RActualCPU.unwrap_err())
        ActualCPU = RActualCPU.unwrap()
        
        Self.assertTrue(ExpectedCPU == ActualCPU)
        
    @unittest.skip("Not implemented")
    def test_ADDI(Self):
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
    
class MemoryUnitTests(unittest.TestCase):
    
    def test_MemoryEquality(Self):
        MemoryA: Memory = Memory(16)
        MemoryB: Memory = Memory(16)
        
        # TODO: Make this test more robust; this doesn't test much at all
        Self.assertTrue(MemoryA == MemoryB)

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

class AssemblerUnitTests(unittest.TestCase):
    
    @unittest.skip("Not a priority right now!")
    def test_Encode_NOP(Self):
        Line = 'nop'
                   # XXXXXX_XXXX_XXXX_XX_XXXXXXXXXXXXXXXX
        Expected = 0b000000_0000_0000_00_0000000000000000
        RActual: Result = Encode(Line)
        if RActual.is_err:
            Self.fail("Failed to encode: {}".format(RActual.unwrap_err))
        Self.assertEqual(Expected, RActual.unwrap())
    
    @unittest.skip("Not a priority right now!")
    def test_Encode_HLT(Self):
        Line = 'hlt'
                   # XXXXXX_XXXX_XXXX_XX_XXXXXXXXXXXXXXXX
        Expected = 0b000001_0000_0000_0000_00000_000000000
        RActual: Result = Encode(Line)
        if RActual.is_err:
            Self.fail("Failed to encode: {}".format(RActual.unwrap_err))
        Self.assertEqual(Expected, RActual.unwrap())

    @unittest.skip("Not a priority right now!")
    def test_Encode_LDI_Hex(Self):
        Line = 'ldi A 0xFFFF'
                   # XXXXXX_XXXX_XXXXXX_XXXXXXXXXXXXXXXX
        Expected = 0b001111_0000_000000_1111111111111111
        RActual: Result = Encode(Line)
        if RActual.is_err:
            Self.fail("Failed to encode: {}".format(RActual.unwrap_err()))
        Self.assertEqual(Expected, RActual.unwrap())

    @unittest.skip("Not a priority right now!")
    def test_Encode_LDI_Octal(Self):
        Line = 'ldi B 0o1720'
                   # XXXXXX_XXXX_XXXXXX_XXXXXXXXXXXXXXXX
        Expected = 0b001111_0001_000000_0000001111010000
        RActual: Result = Encode(Line)
        if RActual.is_err:
            Self.fail("Failed to encode: {}".format(RActual.unwrap_err()))
        Self.assertEqual(Expected, RActual.unwrap())
    
    @unittest.skip("Not a priority right now!")
    def test_Encode_LDI_Binary(Self):
        Line = 'ldi C 0b1101010111010010'
                   # XXXXXX_XXXX_XXXXXX_XXXXXXXXXXXXXXXX
        Expected = 0b001111_0010_000000_1101010111010010
        RActual: Result = Encode(Line)
        if RActual.is_err:
            Self.fail("Failed to encode: {}".format(RActual.unwrap_err()))
        Self.assertEqual(Expected, RActual.unwrap())

    @unittest.skip("Not a priority right now!")
    def test_Encode_LDI_Decimal(Self):
        Line = 'ldi G 16726'
                   # XXXXXX_XXXX_XXXXXX_XXXXXXXXXXXXXXXX
        Expected = 0b001111_0110_000000_0100000101010110
        RActual: Result = Encode(Line)
        if RActual.is_err:
            Self.fail("Failed to encode: {}".format(RActual.unwrap_err()))
        
        Self.assertEqual(Expected, RActual.unwrap())

if __name__ == '__main__':
    unittest.main(verbosity=2)