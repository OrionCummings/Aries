import unittest
from Stack import Stack
from Constants import MAX_STACK_SIZE_IN_BYTES

class StackTests(unittest.TestCase):

    def test_constructor(self):

        stack = Stack()

        self.assertEqual(stack.bytes, [])

    def test_equality_success(self):

        stack1 = Stack()
        stack2 = Stack()

        stack1.bytes = [1,2,3,4,5,6,7,8]
        stack2.bytes = [1,2,3,4,5,6,7,8]

        self.assertEqual(stack1, stack2)

    def test_equality_failure(self):

        stack1 = Stack()
        stack2 = Stack()

        stack1.bytes = [1,2,3,4,5,6,7,8]
        stack2.bytes = [1,2,3,4,5,6,7]

        self.assertNotEqual(stack1, stack2)

    def test_to_string(self):

        stack = Stack()
        stack.bytes = [1,2,3,4,5,6,7,8]

        expected_str = "1,2,3,4,5,6,7,8"
        actual_str = str(stack)

        self.assertEqual(expected_str, actual_str)

    def test_is_empty_success(self):

        stack = Stack()

        self.assertTrue(stack.is_empty())

    def test_is_empty_failure(self):

        stack = Stack()
        stack.bytes = [1,2,3,4,5,6,7,8]

        self.assertFalse(stack.is_empty())

    def test_size(self):

        stack = Stack()
        stack.bytes = [1,2,3,4,5,6,7,8]

        self.assertEqual(stack.size(), 8)

    def test_push(self):

        stack = Stack(8)
        stack.push(1)
        stack.push(2)
        stack.push(3)
        stack.push(4)

        expected_bytes = [n.to_bytes(4, byteorder='little', signed=False) for n in [1,2,3,4]]
        actual_bytes = stack.bytes

        self.assertEqual(expected_bytes, actual_bytes)

    def test_pop(self):

        stack = Stack()
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

        stack = Stack()
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

        stack = Stack()
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

