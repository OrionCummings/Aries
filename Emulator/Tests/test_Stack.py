import unittest
from Stack import Stack
from Constants import MAX_STACK_SIZE_IN_BYTES

class StackTests(unittest.TestCase):

    @staticmethod
    def list_to_little_endian_bytearray(l: list[int]) -> bytearray:
        pass

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

        l = [1]
        stack = Stack(len(l) * 4)

        for n in l:
            stack.push(n)

        actual_bytes = stack.bytes 
        expected_bytes = bytearray(l)

        self.assertEqual(expected_bytes, actual_bytes)

    def test_pop(self):

        stack = Stack(16)
        stack.push(1)
        stack.push(2)
        stack.push(3)
        stack.push(4)
        stack.pop()
        stack.pop()

        expected_bytes = [1,2]
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

        stack = Stack(MAX_STACK_SIZE_IN_BYTES)
        for x in range(0, MAX_STACK_SIZE_IN_BYTES):
            stack.push(x)

        expected_string = "Attempted to push to a full call stack!"
        actual_string = stack.push(256).unwrap_err()

        self.assertEqual(expected_string, actual_string)

    def test_pop_when_empty(self):

        stack = Stack()
        pop_result = stack.pop()

        expected_string = "Attempted to pop from an empty call stack!"
        actual_string = pop_result.unwrap_err()

        self.assertEqual(expected_string, actual_string)

    def test_peek_when_empty(self):

        stack = Stack()
        pop_result = stack.peek()

        expected_string = "Attempted to peek from an empty call stack!"
        actual_string = pop_result.unwrap_err()

        self.assertEqual(expected_string, actual_string)

