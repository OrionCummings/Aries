from __future__ import annotations
from option import Result, Ok
from Constants import MAX_STACK_SIZE_IN_BYTES
from Utilities import trace

class Stack():

    def __init__(self, capacity_in_bytes: int):
        self.capacity = capacity_in_bytes
        self.bytes = bytearray(capacity_in_bytes)
        self.stack_pointer: int = 0
    
    def __eq__(self, other: Stack):
        return self.bytes == other.bytes
    
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
        
        self.stack_pointer += 1
        self.bytes.insert(self.stack_pointer, value)

        # TODO: Fix this inconsistency; maybe convert all
        # Result[bool, str] to Result[None, str] because
        # I rarely care about the value of the bool!
        return Ok(None)

    def pop(self) -> Result[int, str]:
        if self.size() == 0:
            return trace("failed to pop (empty stack)")
        
        value = self.bytes[self.stack_pointer]
        self.stack_pointer += -1

        return Ok(value)

    def peek(self) -> Result[int, str]:
        if self.size() == 0:
            return trace("failed to peek (empty stack)")
        
        value = self.bytes[self.stack_pointer]

        return Ok(value)

if __name__ == '__main__':

    stack = Stack(16)
    print(stack)

