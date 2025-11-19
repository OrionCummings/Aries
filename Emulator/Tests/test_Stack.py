import unittest
from Stack import Stack

class StackTests(unittest.TestCase):

    def test_constructor(self):

        stack = Stack(0)

        self.assertIsInstance(stack, Stack)

    def test_equality_success(self):

        stack1 = Stack(16)
        stack2 = Stack(16)

        l = [255, 12, 241, 0]

        [stack1.push(n) for n in l]
        [stack2.push(n) for n in l]

        self.assertEqual(stack1, stack2)

    def test_equality_failure_capacity(self):

        stack1 = Stack(16)
        stack2 = Stack(16)

        stack1.capacity = stack2.capacity + 1

        self.assertNotEqual(stack1, stack2)

    def test_equality_failure_content(self):

        stack1 = Stack(16)
        stack2 = Stack(16)

        stack1.push(1)

        self.assertNotEqual(stack1, stack2)

    def test_equality_failure_stack_pointer(self):

        stack1 = Stack(16)
        stack2 = Stack(16)

        stack1.stack_pointer = 0
        stack2.stack_pointer = 1

        self.assertNotEqual(stack1, stack2)

    def test_to_string(self):

        stack = Stack(16)

        s = str(stack)

        self.assertIsInstance(s, str)

    def test_is_empty_success(self):

        stack = Stack(1)

        self.assertTrue(stack.is_empty())

    def test_is_empty_failure(self):
        stack = Stack(1)

        stack.push(3)

        self.assertFalse(stack.is_empty())

    def test_size(self):
        stack = Stack(16)

        stack.push(3)

        self.assertEqual(stack.size(), 4)

    def test_push_byte_success(self):
        
        stack = Stack(16)

        r_push_byte = stack.push_byte(255)
        if r_push_byte.is_err:
            self.fail(r_push_byte.unwrap_err())

    def test_pop_byte(self):
        
        expected_pop = 255
        stack = Stack(16)
        stack.push_byte(expected_pop)
        stack_pointer_before = stack.stack_pointer

        r_pop_byte = stack.pop_byte()
        if r_pop_byte.is_err:
            self.fail(r_pop_byte.unwrap_err())

        stack_pointer_after = stack.stack_pointer
        actual_popped = r_pop_byte.unwrap()

        self.assertEqual(expected_pop, actual_popped)
        self.assertTrue(stack_pointer_before + 4, stack_pointer_after)

    def test_peek_byte(self):

        expected_peek = 255
        stack = Stack(16)
        stack.push_byte(expected_peek)

        r_peek_byte = stack.peek_byte()
        if r_peek_byte.is_err:
            self.fail(r_peek_byte.unwrap_err())

        actual_peeked = r_peek_byte.unwrap()
        self.assertEqual(expected_peek, actual_peeked)

    def test_push(self):

        l = [255, 16]
        stack = Stack(len(l) * 4)

        for n in l:
            r_push = stack.push(n)
            if r_push.is_err:
                self.fail(f"unexpected error: '{r_push.unwrap_err()}'")

        # TODO: Make a function that actually calculates this properly.
        expected_bytes = b'\xff\x00\x00\x00\x10\x00\x00\x00'
        actual_bytes = stack.content

        self.assertEqual(expected_bytes, actual_bytes)

    def test_pop(self):

        stack = Stack(16)
        stack.push(1)
        stack.push(2)
        stack.push(3)
        stack.push(4)
        r_popped_value = stack.pop()

        if r_popped_value.is_err:
            self.fail(f"pop failure:\n{r_popped_value.unwrap_err()}")

        actual_value = r_popped_value.unwrap()
        expected_value = 4

        self.assertEqual(expected_value, actual_value)

    def test_peek(self):

        stack = Stack(16)
        stack.push(1)

        expected_result = 1
        r_actual_result = stack.peek()
        if r_actual_result.is_err:
            self.fail("failed to peek stack")

        actual_result = r_actual_result.unwrap()

        self.assertEqual(expected_result, actual_result)

    def test_push_to_full_stack(self):
        
        S = 2

        stack = Stack(S * 4)
        for x in range(0, S):
            r_push = stack.push(x)
            if r_push.is_err:
                self.fail(f"failed to push:\n{r_push.unwrap_err()}")

        r_push_result = stack.push(1)

        if not r_push_result.is_err:
            self.fail(f"expected a failure but got '{r_push_result.unwrap()}'")

        push_result_err = r_push_result.unwrap_err()
        self.assertIsInstance(push_result_err, str)

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

