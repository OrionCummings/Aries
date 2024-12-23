import unittest
from CallStack import CallStack
from Constants import MAX_CALL_STACK_DEPTH

class CallStackTests(unittest.TestCase):

    def test_constructor(self):

        call_stack = CallStack()

        self.assertEqual(call_stack.contents, [])

    def test_equality_success(self):

        call_stack1 = CallStack()
        call_stack2 = CallStack()

        call_stack1.contents = [1,2,3,4,5,6,7,8]
        call_stack2.contents = [1,2,3,4,5,6,7,8]

        self.assertEqual(call_stack1, call_stack2)

    def test_equality_failure(self):

        call_stack1 = CallStack()
        call_stack2 = CallStack()

        call_stack1.contents = [1,2,3,4,5,6,7,8]
        call_stack2.contents = [1,2,3,4,5,6,7]

        self.assertNotEqual(call_stack1, call_stack2)

    def test_to_string(self):

        call_stack = CallStack()
        call_stack.contents = [1,2,3,4,5,6,7,8]

        expected_str = "1,2,3,4,5,6,7,8"
        actual_str = str(call_stack)

        self.assertEqual(expected_str, actual_str)

    def test_is_empty_success(self):

        call_stack = CallStack()

        self.assertTrue(call_stack.is_empty())

    def test_is_empty_failure(self):

        call_stack = CallStack()
        call_stack.contents = [1,2,3,4,5,6,7,8]

        self.assertFalse(call_stack.is_empty())

    def test_size(self):

        call_stack = CallStack()
        call_stack.contents = [1,2,3,4,5,6,7,8]

        self.assertEqual(call_stack.size(), 8)

    def test_push(self):

        call_stack = CallStack()
        call_stack.push(1)
        call_stack.push(2)
        call_stack.push(3)
        call_stack.push(4)

        expected_contents = [1,2,3,4]
        actual_contents = call_stack.contents

        self.assertEqual(expected_contents, actual_contents)

    def test_pop(self):

        call_stack = CallStack()
        call_stack.push(1)
        call_stack.push(2)
        call_stack.push(3)
        call_stack.push(4)
        call_stack.pop()
        call_stack.pop()

        expected_contents = [1,2]
        actual_contents = call_stack.contents

        self.assertEqual(expected_contents, actual_contents)

    def test_peek(self):

        call_stack = CallStack()
        call_stack.push(1)
        call_stack.push(2)
        call_stack.push(3)
        call_stack.push(4)
        call_stack.pop()
        call_stack.pop()

        expected_result = 2
        actual_result = call_stack.peek().unwrap()

        self.assertEqual(expected_result, actual_result)

    def test_push_to_full_call_stack(self):

        call_stack = CallStack()
        for x in range(0, MAX_CALL_STACK_DEPTH):
            call_stack.push(x)

        expected_string = "Attempted to push to a full call stack!"
        actual_string = call_stack.push(256).unwrap_err()

        self.assertEqual(expected_string, actual_string)

    def test_pop_when_empty(self):

        call_stack = CallStack()
        pop_result = call_stack.pop()

        expected_string = "Attempted to pop from an empty call stack!"
        actual_string = pop_result.unwrap_err()

        self.assertEqual(expected_string, actual_string)

    def test_peek_when_empty(self):

        call_stack = CallStack()
        pop_result = call_stack.peek()

        expected_string = "Attempted to peek from an empty call stack!"
        actual_string = pop_result.unwrap_err()

        self.assertEqual(expected_string, actual_string)

