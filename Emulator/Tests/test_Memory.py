import unittest
from Memory import Memory
from Transformations import encode, decode

class MemoryTests(unittest.TestCase):

    def test_memory_constructor(self):
        
        memory = Memory(16)

        self.assertIsInstance(memory, Memory)

    def test_memory_equality_success(self):

        memory1 = Memory(16)
        memory2 = Memory(16)

        self.assertEqual(memory1, memory2)

    def test_memory_equality_failure_capacity(self):

        memory1 = Memory(16)
        memory2 = Memory(17)

        self.assertNotEqual(memory1, memory2)

    def test_memory_equality_failure_content(self):

        memory1 = Memory(16)
        memory2 = Memory(16)

        memory1.set_byte(0, 255)

        self.assertNotEqual(memory1, memory2)

    def test_memory_to_string(self):

        memory = Memory(16)

        s = str(memory)

        self.assertIsInstance(s, str)
    
    def test_memory_get_bytes_success(self):

        memory = Memory(16)
        index = 2
        value = 255
        memory.set_byte(index, value)

        r_get_byte = memory.get_byte(index)
        if r_get_byte.is_err:
            self.fail("failed to get byte")
        
        get_byte = r_get_byte.unwrap()

        self.assertEqual(get_byte, value)

    def test_memory_set_bytes_success(self):

        memory = Memory(16)
        r = range(0, 4)
        value = 255
        expected_bytes = bytearray([value] * len(r))

        r_set_bytes = memory.set_bytes(r, value)
        if r_set_bytes.is_err:
            self.fail("failed to set bytes")

        r_actual_bytes = memory.get_bytes(r)
        if r_actual_bytes.is_err:
            self.fail("failed to get bytes")

        self.assertEqual(expected_bytes, r_actual_bytes.unwrap())

    def test_memory_get_instruction_success(self):

        memory = Memory(16)
        index = 0
        r_expected_instruction = encode('add A G F')
        if r_expected_instruction.is_err:
            self.fail("failed to encode instruction")

        expected_instruction = r_expected_instruction.unwrap()
        memory.set_bytes(range(index, index + 4), expected_instruction)

        r_instruction = memory.get_instruction(index)
        if r_instruction.is_err:
            self.fail("failed to get instruction")

        instruction = r_instruction.unwrap()

        r_actual_instruction = decode(instruction)
        if r_actual_instruction.is_err:
            self.fail("failed to decode instruction")

        actual_instruction = r_actual_instruction.unwrap()

        self.assertEqual(expected_instruction, actual_instruction)



