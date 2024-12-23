from __future__ import annotations

from option import Result, Ok, Err

from Constants import MAX_CALL_STACK_DEPTH

class CallStack():
    """A stack that tracks return addresses."""

    def __init__(self):
        self.contents = []
    
    def __eq__(self, other: CallStack):
        return self.contents == other.contents
    
    def __str__(self):
        return ",".join(str(x) for x in self.contents)

    def is_empty(self) -> bool:
        return self.size() == 0
    
    def size(self) -> bool:
        return len(self.contents)

    def push(self, address: int) -> Result[None, str]:
        if self.size() == MAX_CALL_STACK_DEPTH:
            return Err("Attempted to push to a full call stack!")
        return Ok(self.contents.append(address))

    def pop(self) -> Result[int, str]:
        if self.size() != 0:
            return Ok(self.contents.pop())
        return Err("Attempted to pop from an empty call stack!")

    def peek(self) -> Result[int, str]:
        if self.size() != 0:
            return Ok(self.contents[-1])
        return Err("Attempted to peek from an empty call stack!")
