import unittest
from Transformations import encode, decode

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
        pass

    def test_decode_hlt(self):
        pass

    def test_decode_add(self):
        pass

    def test_decode_addi(self):
        pass

    def test_decode_ldi(self):
        pass

    def test_decode_j(self):
        pass

    # Encode/decode tests
    def test_encode_decode_nop(self):
        pass

    def test_encode_decode_hlt(self):
        pass

    def test_encode_decode_add(self):
        pass

    def test_encode_decode_addi(self):
        pass

    def test_encode_decode_ldi(self):
        pass

    def test_encode_decode_j(self):
        pass

    # Auxilary function tests

if __name__ == '__main__':
    unittest.main()
