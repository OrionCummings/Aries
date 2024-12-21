import unittest
from Instructions import encode

class InstructionTests(unittest.TestCase):
    
    def test_encode_nop(self):
        
        line = 'nop'
        expected_encode = 0
        actual_encode = encode(line).unwrap_or_else(lambda err: self.fail(err))
        
        self.assertEqual(expected_encode, actual_encode)
    
    # def test_encode_hlt(self):
    #     pass
        
    # def test_encode_add(self):
    #     pass
    
    # def test_encode_addi(self):
    #     pass
    
    # def test_encode_ldi(self):
    #     pass
    
    
    
    # def test_decode_nop(self):
    #     pass
    
    # def test_decode_hlt(self):
    #     pass
        
    # def test_decode_add(self):
    #     pass
    
    # def test_decode_addi(self):
    #     pass
    
    # def test_decode_ldi(self):
    #     pass
    
    
    
    # def test_encode_decode(self):
    #     pass
        
    # def test_decode_encode(self):
    #     pass
    
    
    
    # def test_nop(self):
    #     pass

    # def test_hlt(self):
    #     pass
    
    # def test_add(self):
    #     pass
    
    # def test_addi(self):
    #     pass
    
    # def test_ldi(self):
    #     pass

if __name__ == '__main__':
    unittest.main()
