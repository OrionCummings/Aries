import unittest

from option import Result
from Instructions import ADD, NOP, encode, get_opcode
from Memory import Memory
from RegisterFile import RegisterFile
from CPU import CPU
from Constants import *

def print_expected_and_actual_binary(expected: int, actual: int):
    print()
    print("Expected: " + format(expected, "032b"))
    print("Actual:   " + format(actual, "032b"))
    print()

class RegisterFileUnitTests(unittest.TestCase):
    
    def test_RegisterFileEquality(self):
        
        register_file_a: RegisterFile = RegisterFile()
        register_file_b: RegisterFile = RegisterFile()
        
        # TODO: Make this test more robust; this doesn't test much at all
        self.assertTrue(register_file_a == register_file_b)
    
    def test_GetReg(self):
        
        # Create a RegisterFile
        r = RegisterFile()
        
        for reg in REGISTERS.keys():
            r.registers[reg] = 4
        
        for reg in REGISTERS.keys():
            r_value = r.get_reg(reg)
            if r_value.is_err: self.fail(r_value.Err)
            value = r_value.unwrap()
            self.assertEqual(value, 4)
    
    def test_SetReg(self):
        
        # Create a RegisterFile
        r = RegisterFile()
        
        # Set all registers to
        for reg in REGISTERS.keys():
            r.set_reg(reg, 4)
            
            r_value = r.get_reg(reg)
            if r_value.is_err: self.fail(r_value.Err)
            value = r_value.unwrap()
            self.assertEqual(value, 4)
    
    def test_IncrementProgramCounter(self):
        
        # Create a RegisterFile
        R = RegisterFile()
        
        # Increment the instruction pointer
        R.increment_program_counter()
        
        # Check that the value for the instruction pointer is now 1
        self.assertEqual(R.registers['PC'], PC_INC)
    
    def test_IncrementBasePointer(self):
        
        # Create a RegisterFile
        R = RegisterFile()
        
        # Increment the base pointer
        R.increment_base_pointer()
        
        # Check that the value for the base pointer is now 1
        self.assertEqual(R.registers['BP'], BP_INC)
        
    def test_IncrementStackPointer(self):
        
        # Create a RegisterFile
        R = RegisterFile()
        
        # Increment the stack pointer
        R.increment_stack_pointer()
        
        # Check that the value for the stack pointer is now 1
        self.assertEqual(R.registers['SP'], SP_INC)

    def test_FlagRegisterBitPositions(self):
        
        # Create a RegisterFile
        r = RegisterFile()
        
        # Ensure the bit position match the documentation
        self.assertEqual(FL_ZERO, 0)
        self.assertEqual(FL_CARRY, 1)
        self.assertEqual(FL_PARITY, 2)
        self.assertEqual(FL_SIGN, 3)
        self.assertEqual(FL_OVERFLOW, 4)
        self.assertEqual(FL_INTERRUPT, 5)
        self.assertEqual(FL_TRAP, 6)
        self.assertEqual(FL_HPC, 7)
    
    def test_ClearFlags(self):
        
        # Create a RegisterFile
        R = RegisterFile()
        
        # Set the value of the flags register
        R.registers['FL'] = int(0b0000000111111111)
        
        # Clear the flags register
        R.clear_flags()
        
        # Check that the value for the flag register is zero
        self.assertEqual(r.registers['FL'], 0)
    
    def test_SetFlag(self):
        
        # Create a RegisterFile
        r = RegisterFile()
        
        # Set all flags
        r.set_flag(FL_ZERO)
        r.set_flag(FL_CARRY)
        r.set_flag(FL_PARITY)
        r.set_flag(FL_SIGN)
        r.set_flag(FL_OVERFLOW)
        r.set_flag(FL_INTERRUPT)
        r.set_flag(FL_TRAP)
        r.set_flag(FL_HPC)
        
        # Check that the value for the flag register is zero
        self.assertEqual(r.registers['FL'], int(0b0000000011111111))

    def test_GetFlag(self):
        
        # Create a RegisterFile
        r = RegisterFile()
        
        # Set the flags register
        r.registers['FL'] = int(0x000000FF)
        
        # Get all flags
        zero_value = r.GetFlag(FL_ZERO)
        carry_value = r.GetFlag(FL_CARRY)
        parity_value = r.GetFlag(FL_PARITY)
        sign_value = r.GetFlag(FL_SIGN)
        overflow_value = r.GetFlag(FL_OVERFLOW)
        interrupt_value = r.GetFlag(FL_INTERRUPT)
        trap_value = r.GetFlag(FL_TRAP)
        hpc_value = r.GetFlag(FL_HPC)
        
        # Check that the values match
        self.assertEqual(zero_value, 1)
        self.assertEqual(carry_value, 1)
        self.assertEqual(parity_value, 1)
        self.assertEqual(sign_value, 1)
        self.assertEqual(overflow_value, 1)
        self.assertEqual(interrupt_value, 1)
        self.assertEqual(trap_value, 1)
        self.assertEqual(hpc_value, 1)

    def test_ToggleFlag(self):
        
        # Create a RegisterFile
        r = RegisterFile()

        # Set the flags register
        r.registers['FL'] = int(0x000000FF)
        
        # Toggle all flags
        r.toggle_flag(FL_ZERO)
        r.toggle_flag(FL_CARRY)
        r.toggle_flag(FL_PARITY)
        r.toggle_flag(FL_SIGN)
        r.toggle_flag(FL_OVERFLOW)
        r.toggle_flag(FL_INTERRUPT)
        r.toggle_flag(FL_TRAP)
        r.toggle_flag(FL_HPC)
        
        # Check that the value for the flag register is zero
        self.assertEqual(r.registers['FL'], int(0x00000000))

class CPUUnitTests(unittest.TestCase):
    
    def test_CPUEquality(self):
        
        cpu_a = CPU(16, 16)
        cpu_b = CPU(16, 16)
        
        # TODO: Make this test more robust; this doesn't test much at all
        self.assertTrue(cpu_a == cpu_b)

class InstructionUnitTests(unittest.TestCase):
    
    def test_NOP(self):
        original_cpu: CPU = CPU(16, 16)
        expected_cpu: CPU = CPU(16, 16)
        
        line = 'nop'
        r_instruction = encode(line)
        if r_instruction.is_err: self.fail(r_instruction.Err())
        instruction = r_instruction.unwrap()
        
        r_actual_cpu = NOP(original_cpu, instruction)
        if r_actual_cpu.is_err: self.fail(r_actual_cpu.Err())
        actual_cpu = r_actual_cpu.unwrap()
        
        self.assertTrue(expected_cpu == actual_cpu)
    
    def test_ADD(self):
        
        # NOTE: These tests aren't amazing and they actually could use
        # opcode information from the Encode() call.
        
        original_cpu = CPU(16, 16)
        expected_cpu = CPU(16, 16)
        expected_cpu.register_file.registers['A'] = 4
        expected_cpu.register_file.registers['B'] = 3
        expected_cpu.register_file.registers['C'] = 7
        
        line = 'add A B C'
        r_instruction = encode(line)
        if r_instruction.is_err: self.fail(r_instruction.unwrap_err())
        instruction = r_instruction.unwrap()
        
        r_actual_cpu = ADD(original_cpu, instruction)
        if r_actual_cpu.is_err: self.fail(r_actual_cpu.unwrap_err())
        actual_cpu = r_actual_cpu.unwrap()
        
        self.assertTrue(expected_cpu == actual_cpu)
        
    @unittest.skip("Not implemented")
    def test_ADDI(self):
        self.fail()
        
    @unittest.skip("Not implemented")
    def test_SUB(self):
        self.fail()
        
    @unittest.skip("Not implemented")
    def test_AND(self):
        self.fail()
        
    @unittest.skip("Not implemented")
    def test_OR(self):
        self.fail()
        
    @unittest.skip("Not implemented")
    def test_NOT(self):
        self.fail()
        
    @unittest.skip("Not implemented")
    def test_SHR(self):
        self.fail()
        
    @unittest.skip("Not implemented")
    def test_SHL(self):
        self.fail()
    
class MemoryUnitTests(unittest.TestCase):
    
    def test_MemoryEquality(self):
        memory_a = Memory(16)
        memory_b = Memory(16)
        
        # TODO: Make this test more robust; this doesn't test much at all
        self.assertTrue(memory_a == memory_b)

class AssemblerFunctionUnitTests(unittest.TestCase):
    
    def OpcodeComparison(self, expected: int, line: str):
        r_actual = get_opcode(line)
        actual = r_actual.unwrap_or_else(lambda: self.fail("Failed to parse opcode"))
        self.assertEqual(expected, actual)
        
    def test_GetOpcodeNOP(self):
        line = 'nop'
        expected = OPCODES['nop']
        self.OpcodeComparison(expected, line)
        
    def test_GetOpcodeHLT(self):
        line = 'hlt'
        expected = OPCODES['hlt']
        self.OpcodeComparison(expected, line)

    def test_GetOpcodeADD(self):
        line = 'add A B C'
        expected = OPCODES['add']
        self.OpcodeComparison(expected, line)
        
    def test_GetOpcodeADDI(self):
        line = 'addi A B 28921'
        expected = OPCODES['addi']
        self.OpcodeComparison(expected, line)

class AssemblerUnitTests(unittest.TestCase):
    
    @unittest.skip("Not a priority right now!")
    def test_Encode_NOP(self):
        line = 'nop'
                   # XXXXXX_XXXX_XXXX_XX_XXXXXXXXXXXXXXXX
        expected = 0b000000_0000_0000_00_0000000000000000
        r_actual: Result = encode(line)
        if r_actual.is_err:
            self.fail("Failed to encode: {}".format(r_actual.unwrap_err))
        self.assertEqual(expected, r_actual.unwrap())
    
    @unittest.skip("Not a priority right now!")
    def test_Encode_HLT(self):
        line = 'hlt'
                   # XXXXXX_XXXX_XXXX_XX_XXXXXXXXXXXXXXXX
        expected = 0b000001_0000_0000_0000_00000_000000000
        r_actual: Result = encode(line)
        if r_actual.is_err:
            self.fail("Failed to encode: {}".format(r_actual.unwrap_err))
        self.assertEqual(expected, r_actual.unwrap())

    @unittest.skip("Not a priority right now!")
    def test_Encode_LDI_Hex(self):
        line = 'ldi A 0xFFFF'
                   # XXXXXX_XXXX_XXXXXX_XXXXXXXXXXXXXXXX
        expected = 0b001111_0000_000000_1111111111111111
        r_actual: Result = encode(line)
        if r_actual.is_err:
            self.fail("Failed to encode: {}".format(r_actual.unwrap_err()))
        self.assertEqual(expected, r_actual.unwrap())

    @unittest.skip("Not a priority right now!")
    def test_Encode_LDI_Octal(self):
        line = 'ldi B 0o1720'
                   # XXXXXX_XXXX_XXXXXX_XXXXXXXXXXXXXXXX
        expected = 0b001111_0001_000000_0000001111010000
        r_actual: Result = encode(line)
        if r_actual.is_err:
            self.fail("Failed to encode: {}".format(r_actual.unwrap_err()))
        self.assertEqual(expected, r_actual.unwrap())
    
    @unittest.skip("Not a priority right now!")
    def test_Encode_LDI_Binary(self):
        line = 'ldi C 0b1101010111010010'
                   # XXXXXX_XXXX_XXXXXX_XXXXXXXXXXXXXXXX
        expected = 0b001111_0010_000000_1101010111010010
        r_actual: Result = encode(line)
        if r_actual.is_err:
            self.fail("Failed to encode: {}".format(r_actual.unwrap_err()))
        self.assertEqual(expected, r_actual.unwrap())

    @unittest.skip("Not a priority right now!")
    def test_Encode_LDI_Decimal(self):
        line = 'ldi G 16726'
                   # XXXXXX_XXXX_XXXXXX_XXXXXXXXXXXXXXXX
        expected = 0b001111_0110_000000_0100000101010110
        r_actual: Result = encode(line)
        if r_actual.is_err:
            self.fail("Failed to encode: {}".format(r_actual.unwrap_err()))
        
        self.assertEqual(expected, r_actual.unwrap())

if __name__ == '__main__':
    unittest.main(verbosity=2)