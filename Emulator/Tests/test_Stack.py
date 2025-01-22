import unittest
from Stack import Stack
from Constants import MAX_STACK_SIZE_IN_BYTES

class StackTests(unittest.TestCase):

    def test_constructor(self):

        stack = Stack(0)
        a = bytearray(0)

        self.assertEqual(stack.bytes, a)

    def test_equality_success(self):

        stack1 = Stack()
        stack2 = Stack()

        l = [1,2,3,4]

        stack1.capacity = len(l) * 4
        stack2.capacity = len(l) * 4

        stack1.bytes = StackTests.list_to_little_endian_bytes(l)
        stack2.bytes = StackTests.list_to_little_endian_bytes(l)

        self.assertEqual(stack1, stack2)

    def test_equality_failure_capacity(self):

        stack1 = Stack()
        stack2 = Stack()

        l = [1,2,3,4]

        stack1.capacity = len(l) * 4
        stack2.capacity = (len(l) * 4) - 1

        stack1.bytes = StackTests.list_to_little_endian_bytes(l)
        stack2.bytes = StackTests.list_to_little_endian_bytes(l)

        self.assertNotEqual(stack1, stack2)

    def test_equality_failure_content(self):

        stack1 = Stack()
        stack2 = Stack()

        l1 = [1,2,3,4]
        l2 = [1,2,3]

        stack1.capacity = len(l1) * 4
        stack2.capacity = len(l2) * 4

        stack1.bytes = StackTests.list_to_little_endian_bytes(l1)
        stack2.bytes = StackTests.list_to_little_endian_bytes(l2)

        self.assertNotEqual(stack1, stack2)

    def test_equality_failure_stack_pointer(self):

        stack1 = Stack()
        stack2 = Stack()

        l = [1,2,3,4]

        stack1.capacity = len(l) * 4
        stack2.capacity = len(l) * 4

        stack1.bytes = StackTests.list_to_little_endian_bytes(l)
        stack2.bytes = StackTests.list_to_little_endian_bytes(l)

        stack1.stack_pointer = 0
        stack2.stack_pointer = 1

        self.assertNotEqual(stack1, stack2)

    def test_to_string(self):

        l = [1,2,3,4]
        stack = Stack(len(l) * 4)
        for n in l:
            stack.push(n)

        expected_str = "00 00 00 01 00 00 00 02 00 00 00 03 00 00 00 04"
        actual_str = str(stack).replace('\n', "") # Remove newlines to make this render-target-independent

        self.assertEqual(expected_str, actual_str)

    def test_is_empty_success(self):

        stack = Stack(1)

        self.assertTrue(stack.is_empty())

    def test_is_empty_failure(self):

        stack = Stack(1)
        stack.bytes = StackTests.list_to_little_endian_bytes([1,2,3,4])

        self.assertFalse(stack.is_empty())

    def test_size(self):

        stack = Stack(16)
        stack.bytes = StackTests.list_to_little_endian_bytes([1,2,3,4])

        self.assertEqual(stack.size(), 8)

    def test_push(self):

        l = [255, 16]
        stack = Stack(len(l) * 4)

        for n in l:
            stack.push(n)

        # TODO: Make a function that actually calculates this properly.
        expected_bytes = b'\xff\x00\x00\x00\x10\x00\x00\x00'
        actual_bytes = stack.bytes

        self.assertEqual(expected_bytes, actual_bytes)

    def test_pop(self):

        stack = Stack(16)
        stack.push(1)
        stack.push(2)
        stack.push(3)
        stack.push(4)
        stack.pop()
        stack.pop()

        expected_bytes = bytearray(b'\x01\x00\x00\x00\x02\x00\x00\x00')
        actual_bytes = stack.bytes

        self.assertEqual(expected_bytes, actual_bytes)

    def test_peek(self):

        stack = Stack(16)
        stack.push(1)
        stack.push(2)
        stack.push(3)
        stack.push(4)
        stack.pop()
        stack.pop()

        expected_result = 2
        actual_result = stack.peek().unwrap()

        self.assertEqual(expected_result, actual_result)

    def test_push_to_full_stack(self):
        
        S = 2

        stack = Stack(S)
        for x in range(0, S):
            stack.push(x)

        r_push_result = stack.push(1)

        if not r_push_result.is_err:
            self.fail(f"expected a failure but got '{r_push_result.unwrap()}'")

        push_result = r_push_result.unwrap_err()
        self.assertIsInstance(push_result, str)

    def test_pop_when_empty(self):

        stack = Stack(0)
        r_pop_result = stack.pop()

        if not r_pop_result.is_err:
            self.fail(f"expected a failure but got '{r_pop_result.unwrap()}'")

        pop_result = r_pop_result.unwrap_err()
        self.assertIsInstance(pop_result, str)

    def test_peek_when_empty(self):

        stack = Stack(0)
        r_peek_result = stack.peek()

        if not r_peek_result.is_err:
            self.fail(f"expected a failure but got '{r_peek_result.unwrap()}'")

        peek_result = r_peek_result.unwrap_err()
        self.assertIsInstance(peek_result, str)

