import unittest
from Transformations import encode, decode, get_opcode, is_valid_opcode

class TransformationTests(unittest.TestCase):
    
    # Encode tests
    def test_encode_nop(self):
        line = "nop"
        actual_encoded_line = encode(line).unwrap_or_else(lambda e: self.fail(e))
        expected_encoded_line = int("000000 00000000000000000000000000".replace(" ", ""), 2)
        self.assertEqual(expected_encoded_line, actual_encoded_line)

    def test_encode_hlt(self):
        line = "hlt"
        actual_encoded_line = encode(line).unwrap_or_else(lambda e: self.fail(e))
        expected_encoded_line = int("000001 00000000000000000000000000".replace(" ", ""), 2)
        self.assertEqual(expected_encoded_line, actual_encoded_line)

    def test_encode_add(self):
        line = "add A B C"
        actual_encoded_line = encode(line).unwrap_or_else(lambda e: self.fail(e))
        expected_encoded_line = int("000010 0000 0001 0010 00000 000000000".replace(" ", ""), 2)
        self.assertEqual(expected_encoded_line, actual_encoded_line)

    def test_encode_addi(self):
        line = "addi 267 C"
        actual_encoded_line = encode(line).unwrap_or_else(lambda e: self.fail(e))
        expected_encoded_line = int("000011 0010 0000 00 0000000100001011".replace(" ", ""), 2)
        self.assertEqual(expected_encoded_line, actual_encoded_line)

    def test_encode_ldi(self):
        line = "ldi 267 I"
        actual_encoded_line = encode(line).unwrap_or_else(lambda e: self.fail(e))
        expected_encoded_line = int("001111 1000 0000 00 0000000100001011".replace(" ", ""), 2)
        self.assertEqual(expected_encoded_line, actual_encoded_line)

    def test_encode_j(self):
        line = "j 23742"
        actual_encoded_line = encode(line).unwrap_or_else(lambda e: self.fail(e))
        expected_encoded_line = int("010110 00000000000101110010111110".replace(" ", ""), 2)
        self.assertEqual(expected_encoded_line, actual_encoded_line)

    # Decode tests
    def test_decode_nop(self):
        encoded_instruction = int("000000 00000000000000000000000000".replace(" ", ""), 2)
        actual_decoded_line = decode(encoded_instruction).unwrap_or_else(lambda e: self.fail(e))
        expected_decoded_line = "nop"
        self.assertEqual(expected_decoded_line, actual_decoded_line)

    def test_decode_hlt(self):
        encoded_instruction = int("000001 00000000000000000000000000".replace(" ", ""), 2)
        actual_decoded_line = decode(encoded_instruction).unwrap_or_else(lambda e: self.fail(e))
        expected_decoded_line = "hlt"
        self.assertEqual(expected_decoded_line, actual_decoded_line)

    def test_decode_add(self):
        encoded_instruction = int("000010 0000 0001 0010 00000 000000000".replace(" ", ""), 2)
        actual_decoded_line = decode(encoded_instruction).unwrap_or_else(lambda e: self.fail(e))
        expected_decoded_line = "add A B C"
        self.assertEqual(expected_decoded_line, actual_decoded_line)

    def test_decode_addi(self):
        encoded_instruction = int("000011 0010 0000 00 0000000100001011".replace(" ", ""), 2)
        actual_decoded_line = decode(encoded_instruction).unwrap_or_else(lambda e: self.fail(e))
        expected_decoded_line = "addi 267 C"
        self.assertEqual(expected_decoded_line, actual_decoded_line)

    def test_decode_ldi(self):
        encoded_instruction = int("001111 1000 0000 00 0000000100001011".replace(" ", ""), 2)
        actual_decoded_line = decode(encoded_instruction).unwrap_or_else(lambda e: self.fail(e))
        expected_decoded_line = "ldi 267 I"
        self.assertEqual(expected_decoded_line, actual_decoded_line)

    def test_decode_j(self):
        encoded_instruction = int("010110 00000000000101110010111110".replace(" ", ""), 2)
        actual_decoded_line = decode(encoded_instruction).unwrap_or_else(lambda e: self.fail(e))
        expected_decoded_line = "j 23742"
        self.assertEqual(expected_decoded_line, actual_decoded_line)

    # Encode/decode tests
    def test_encode_decode_nop(self):
        expected_line = "nop"
        encoded_line = encode(expected_line).unwrap()
        decoded_line = decode(encoded_line).unwrap()
        self.assertEqual(expected_line, decoded_line)

    def test_encode_decode_hlt(self):
        expected_line = "hlt"
        encoded_line = encode(expected_line).unwrap()
        decoded_line = decode(encoded_line).unwrap()
        self.assertEqual(expected_line, decoded_line)

    def test_encode_decode_add(self):
        expected_line = "add A B C"
        encoded_line = encode(expected_line).unwrap()
        decoded_line = decode(encoded_line).unwrap()
        self.assertEqual(expected_line, decoded_line)

    def test_encode_decode_addi(self):
        expected_line = "addi 267 C"
        encoded_line = encode(expected_line).unwrap()
        decoded_line = decode(encoded_line).unwrap()
        self.assertEqual(expected_line, decoded_line)

    def test_encode_decode_ldi(self):
        expected_line = "ldi 267 I"
        encoded_line = encode(expected_line).unwrap()
        decoded_line = decode(encoded_line).unwrap()
        self.assertEqual(expected_line, decoded_line)

    def test_encode_decode_j(self):
        expected_line = "j 23742"
        encoded_line = encode(expected_line).unwrap()
        decoded_line = decode(encoded_line).unwrap()
        self.assertEqual(expected_line, decoded_line)

    # Auxilary function tests
    def test_get_opcode_from_string_success(self):
        instruction: str = "add"
        actual_opcode = get_opcode(instruction).unwrap()
        expected_opcode: str = "add"
        self.assertEqual(expected_opcode, actual_opcode)

    def test_get_opcode_from_int_success(self):
        instruction: int = 2**32 - 1
        actual_opcode = get_opcode(instruction).unwrap()
        expected_opcode: int = 2**6 - 1
        self.assertEqual(expected_opcode, actual_opcode)

    def test_get_opcode_from_bad_type_failure(self):
        instruction: dict = {}
        bad_instruction_response = get_opcode(instruction)
        self.assertTrue(bad_instruction_response.is_err)

    def test_is_valid_opcode(self):
        self.assertTrue(is_valid_opcode("nop"))
        self.assertTrue(is_valid_opcode("hlt"))
        self.assertTrue(is_valid_opcode("add"))
        self.assertTrue(is_valid_opcode("addi"))
        self.assertTrue(is_valid_opcode("ldi"))
        self.assertTrue(is_valid_opcode("j"))
        self.assertTrue(is_valid_opcode("ret"))

        self.assertFalse(is_valid_opcode("1"))
        self.assertFalse(is_valid_opcode("a"))
        self.assertFalse(is_valid_opcode("n9pawervy8"))
        self.assertFalse(is_valid_opcode("beef"))
        self.assertFalse(is_valid_opcode("syscall"), "what the fuck are you doing!??")
