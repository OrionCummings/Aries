from __future__ import annotations
from option import Result, Ok
from ByteBank import ByteBank
from Utilities import trace
from Types import RegisterValue

class Stack(ByteBank):

    def __init__(self, capacity_in_bytes: int):
        super().__init__(capacity_in_bytes)

        self.stack_pointer: int = 0

    def __eq__(self, other: Stack):
        return isinstance(other, Stack) and \
            (type(self), self.capacity, self.stack_pointer, self.content) == (type(other), other.capacity, other.stack_pointer, other.content)

    def __str__(self) -> str:
        return super().__str__()

    def set_stack_memory_boundary(self, boundary: range) -> Stack:
        self.stack_memory_boundary = boundary
        return self

    def update_stack_pointer(self, new_stack_pointer: int) -> None:
        self.stack_pointer = new_stack_pointer

    def is_empty(self) -> bool:
        return self.size() == 0
    
    def size(self) -> int:
        return self.stack_pointer

    def push_byte(self, value: int) -> Result[None, str]:
        if value not in range(0, 256):
            return trace(f"value '{value}' is out of range")
        
        r_set_byte = super().set_byte(self.stack_pointer, value)
        if r_set_byte.is_err:
            return trace(r_set_byte.unwrap_err())

        self.stack_pointer += 1

        return Ok(None)

    def pop_byte(self) -> Result[int, str]:
        if self.size() == 0:
            return trace("cannot pop byte from empty stack")
        
        r_get_byte = super().get_byte(self.stack_pointer-1)
        if r_get_byte.is_err:
            return trace("failed to get byte", r_get_byte.unwrap_err())
        
        self.stack_pointer -= 1
        
        super().set_byte(self.stack_pointer, 0)

        return Ok(r_get_byte.unwrap())

    def peek_byte(self) -> Result[int, str]:
        if self.size() == 0:
            return trace("cannot peek from empty stack")
        
        r_get_byte = super().get_byte(self.stack_pointer-1)
        if r_get_byte.is_err:
            return trace("failed to get byte", r_get_byte.unwrap_err())

        return Ok(r_get_byte.unwrap())

    def push(self, value: int) -> Result[None, str]:
        if self.stack_pointer >= self.capacity:
            return trace("cannot push onto full stack")
        
        # Split `value` into four bytes
        value_bytes = value.to_bytes(4, byteorder='little', signed=False)

        for byt in value_bytes:
            self.push_byte(byt)

        return Ok(None)

    def pop(self) -> Result[int, str]:
        
        if self.size() <= 0:
            return trace("cannot pop from empty stack")
        
        r_value = self.peek()
        if r_value.is_err:
            return trace("failed to peek value", r_value.unwrap_err())

        value = r_value.unwrap()

        # Reduce the stack pointer because we just popped off a value
        self.stack_pointer -= 4

        # Push a zero in the old value's place
        self.push(0)

        # Reduce the stack pointer again because the previous zero push
        # increased it
        self.stack_pointer -= 4

        return Ok(value)

    def peek(self) -> Result[int, str]:
        if self.size() == 0:
            return trace("failed to peek (empty stack)")
        
        r_byte1 = self.pop_byte()
        r_byte2 = self.pop_byte()
        r_byte3 = self.pop_byte()
        r_byte4 = self.pop_byte()
        
        error_message = "failed to pop byte" # Linter wanted it; fine
        if r_byte1.is_err: return trace(error_message, r_byte1.unwrap_err())
        if r_byte2.is_err: return trace(error_message, r_byte2.unwrap_err())
        if r_byte3.is_err: return trace(error_message, r_byte3.unwrap_err())
        if r_byte4.is_err: return trace(error_message, r_byte4.unwrap_err())

        byte1 = r_byte1.unwrap()
        byte2 = r_byte2.unwrap()
        byte3 = r_byte3.unwrap()
        byte4 = r_byte4.unwrap()

        little_endian_bytes = [byte4, byte3, byte2, byte1]
        value = int.from_bytes(little_endian_bytes, byteorder='little', signed=False)

        return Ok(value)
