import unittest
from ByteBank import ByteBank, ByteBankSettings

class ByteBankTests(unittest.TestCase):

    def test_byte_bank_settings_equality_success(self):

        settings1 = ByteBankSettings()
        settings2 = ByteBankSettings()

        self.assertEqual(settings1, settings2)

    def test_byte_bank_settings_equality_failure_capacity(self):

        settings1 = ByteBankSettings()
        settings2 = ByteBankSettings()
        settings2.capacity = settings1.capacity + 1

        self.assertNotEqual(settings1, settings2)

    def test_byte_bank_settings_equality_failure_print_num_rows(self):

        settings1 = ByteBankSettings()
        settings2 = ByteBankSettings()
        settings2.print_num_rows = settings1.print_num_rows + 1

        self.assertNotEqual(settings1, settings2)

    def test_byte_bank_settings_equality_failure_capacity_and_print_num_rows(self):

        settings1 = ByteBankSettings()
        settings2 = ByteBankSettings()
        settings2.capacity = settings1.capacity + 1
        settings2.print_num_rows = settings1.print_num_rows + 1

        self.assertNotEqual(settings1, settings2)

    def test_byte_bank_constructor(self):

        bank = ByteBank(ByteBankSettings())

        self.assertIsInstance(bank, ByteBank)

    def test_byte_bank_equality_success(self):
        
        bank1 = ByteBank(ByteBankSettings())
        bank2 = ByteBank(ByteBankSettings())

        self.assertEqual(bank1, bank2)

    def test_byte_bank_equality_failure_capacity(self):
        
        settings1 = ByteBankSettings()
        settings2 = ByteBankSettings()
        settings2.capacity = settings1.capacity+1

        bank1 = ByteBank(settings1)
        bank2 = ByteBank(settings2)

        self.assertNotEqual(bank1, bank2)

    def test_byte_bank_equality_failure_print_num_rows(self):
        
        settings1 = ByteBankSettings()
        settings2 = ByteBankSettings()
        settings2.print_num_rows = settings1.print_num_rows+1

        bank1 = ByteBank(settings1)
        bank2 = ByteBank(settings2)

        self.assertNotEqual(bank1, bank2)

    def test_byte_bank_equality_failure_content(self):
        
        bank1 = ByteBank(ByteBankSettings())
        bank2 = ByteBank(ByteBankSettings())
        bank2.content[0] = 255

        self.assertNotEqual(bank1, bank2)

    def test_byte_bank_str(self):

        bank = ByteBank(ByteBankSettings())

        s = str(bank)

        self.assertIsInstance(s, str)

    def test_byte_bank_get_byte_success(self):

        bank = ByteBank(ByteBankSettings())

        r_get_byte = bank.get_byte(0)

        if r_get_byte.is_err:
            self.fail(f"failed to get byte: {r_get_byte.unwrap_err()}")

        actual_byte = r_get_byte.unwrap()
        expected_byte = 0

        self.assertEqual(actual_byte, expected_byte)

    def test_byte_bank_get_byte_failure_index_too_small(self):

        bank = ByteBank(ByteBankSettings())

        r_get_byte = bank.get_byte(-1)

        if not r_get_byte.is_err:
            self.fail("failure expected but not received")

    def test_byte_bank_get_byte_failure_index_too_large(self):

        bank = ByteBank(ByteBankSettings())
        index = bank.capacity

        r_get_byte = bank.get_byte(index)

        if not r_get_byte.is_err:
            self.fail("failure expected but not received")

    def test_byte_bank_get_bytes_success_range(self):

        bank = ByteBank(ByteBankSettings())
        r = range(0,2)

        r_get_bytes = bank.get_bytes(r)
        if r_get_bytes.is_err:
            self.fail(r_get_bytes.unwrap_err())

        actual_get_bytes = r_get_bytes.unwrap()
        expected_get_bytes = bytearray([0, 0])

        self.assertEqual(actual_get_bytes, expected_get_bytes)

    def test_byte_bank_get_bytes_success_list(self):

        bank = ByteBank(ByteBankSettings())
        r = [0, 1, 2]

        r_get_bytes = bank.get_bytes(r)
        if r_get_bytes.is_err:
            self.fail(r_get_bytes.unwrap_err())

        actual_get_bytes = r_get_bytes.unwrap()
        expected_get_bytes = bytearray([0, 0, 0])

        self.assertEqual(actual_get_bytes, expected_get_bytes)

    def test_byte_bank_get_bytes_failure_failed_to_get_bytes(self):

        bank = ByteBank(ByteBankSettings())
        r = [0, 1, -1]

        r_get_bytes = bank.get_bytes(r)
        if not r_get_bytes.is_err:
            self.fail("failure expected but not received")

    def test_byte_bank_set_byte_success(self):

        bank = ByteBank(ByteBankSettings())
        index = 0
        value = 255

        r_set_byte = bank.set_byte(index, value)
        
        if r_set_byte.is_err:
            self.fail(r_set_byte.unwrap_err())

        actual_value = bank.content[index]
        expected_value = value

        self.assertEqual(expected_value, actual_value)

    def test_byte_bank_set_byte_failure_index_too_small(self):

        bank = ByteBank(ByteBankSettings())
        index = -1
        value = 255

        r_set_byte = bank.set_byte(index, value)
        
        if not r_set_byte.is_err:
            self.fail("failure expected but not received")

    def test_byte_bank_set_byte_failure_index_too_large(self):

        bank = ByteBank(ByteBankSettings())
        index = bank.capacity
        value = 255

        r_set_byte = bank.set_byte(index, value)
        
        if not r_set_byte.is_err:
            self.fail("failure expected but not received")

    def test_byte_bank_set_byte_failure_value_too_small(self):

        bank = ByteBank(ByteBankSettings())
        index = 0
        value = -1

        r_set_byte = bank.set_byte(index, value)
        
        if not r_set_byte.is_err:
            self.fail("failure expected but not received")

    def test_byte_bank_set_byte_failure_value_too_large(self):

        bank = ByteBank(ByteBankSettings())
        index = 0
        value = 256

        r_set_byte = bank.set_byte(index, value)
        
        if not r_set_byte.is_err:
            self.fail("failure expected but not received")

    def test_byte_bank_set_bytes_success_range(self):

        bank = ByteBank(ByteBankSettings())
        indices = range(4,6)
        values = [255, 255]

        r_set_bytes = bank.set_bytes(indices, values)
        
        if r_set_bytes.is_err:
            self.fail(r_set_bytes.unwrap_err())

        for (vindex, cindex) in enumerate(indices):
            actual_value = bank.content[cindex]
            expected_value = values[vindex]

            self.assertEqual(expected_value, actual_value)

    def test_byte_bank_set_bytes_success_list(self):

        bank = ByteBank(ByteBankSettings())
        indices = [3, 4, 5]
        values = [255, 255, 255]

        r_set_bytes = bank.set_bytes(indices, values)
        
        if r_set_bytes.is_err:
            self.fail(r_set_bytes.unwrap_err())

        for (vindex, cindex) in enumerate(indices):
            actual_value = bank.content[cindex]
            expected_value = values[vindex]

            self.assertEqual(expected_value, actual_value)

    def test_byte_bank_set_bytes_success_single_value(self):

        bank = ByteBank(ByteBankSettings())
        indices = [3, 4, 5]
        values = 255

        r_set_bytes = bank.set_bytes(indices, values)
        
        if r_set_bytes.is_err:
            self.fail(r_set_bytes.unwrap_err())

        for (vindex, cindex) in enumerate(indices):
            actual_value = bank.content[cindex]
            expected_value = 255

            self.assertEqual(expected_value, actual_value)

    def test_byte_bank_set_bytes_failure_range_and_value_length_differ(self):

        bank = ByteBank(ByteBankSettings())
        indices = [3, 4, 5]
        values = [255, 255]

        r_set_bytes = bank.set_bytes(indices, values)
        
        if not r_set_bytes.is_err:
            self.fail("failure expected but not received")

    def test_byte_bank_set_bytes_failure_failed_to_set_byte(self):

        bank = ByteBank(ByteBankSettings())
        indices = [3, 4, bank.capacity]
        values = [255, 255, 0]

        r_set_bytes = bank.set_bytes(indices, values)
        
        if not r_set_bytes.is_err:
            self.fail("failure expected but not received")



