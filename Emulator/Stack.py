from __future__ import annotations
import struct
from option import Result, Ok
from Constants import MAX_STACK_SIZE_IN_BYTES
from Utilities import trace

class Stack():

    def __init__(self, capacity_in_bytes: int = 0):
        self.capacity = capacity_in_bytes
        self.bytes = bytearray(capacity_in_bytes)

        # TODO: Sync this with cpu stack pointer!!!!!!!!!!!!!!!!!!
        self.stack_pointer: int = 0

    def __eq__(self, other: Stack):
        return (self.capacity == other.capacity and self.bytes == other.bytes and self.stack_pointer == other.stack_pointer)

    def __str__(self):

        builder: str = ""
        for index in range(0, self.capacity):
            
            # TODO: Magic number!
            if index != 0 and index % 16 == 0:
                builder += "\n"
            
            builder += "{:02X}".format(self.bytes[index])
            builder += " "

        builder += '\n'
        return builder

    def is_empty(self) -> bool:
        return self.size() == 0
    
    def size(self) -> int:
        return len(self.bytes)

    def push(self, value: int) -> Result[None, str]:
        if self.size() >= MAX_STACK_SIZE_IN_BYTES:
            return trace(f"failed to push '{value}' (full stack)")
        
        value_bytes = value.to_bytes(4, byteorder='little', signed=False)

        # TODO: Magic number!
        # Insert each byte into the stack
        for index in range(0, 4):
            self.bytes[self.stack_pointer] = value_bytes[index]
            self.stack_pointer += 1

        # TODO: Fix this inconsistency; maybe convert all
        # Result[bool, str] to Result[None, str] because
        # I rarely care about the value of the bool!
        return Ok(None)

    def pop(self) -> Result[int, str]:
        if self.size() == 0:
            return trace("failed to pop (empty stack)")
        
        byte1 = self.bytes[self.stack_pointer]
        byte2 = self.bytes[self.stack_pointer-1]
        byte3 = self.bytes[self.stack_pointer-2]
        byte4 = self.bytes[self.stack_pointer-3]
        parts = [byte1, byte2, byte3, byte4]

        try:
            packed_bytes = struct.pack('>BBBB', *parts)
        except struct.error as _:
            return trace(f"failed to pack bytes")
        
        value = int.from_bytes(packed_bytes, byteorder='little', signed=False)

        self.stack_pointer -= 4

        return Ok(value)

    def peek(self) -> Result[int, str]:
        if self.size() == 0:
            return trace("failed to peek (empty stack)")
        
        value = self.bytes[self.stack_pointer]

        return Ok(value)

if __name__ == '__main__':

    #TODO: Fix push and pop! THey don't play nicely with the byte conversion!

    stack = Stack(16)
    print(stack)
    stack.push(255)
    print(stack)
    stack.pop()
    print(stack)

