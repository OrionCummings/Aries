from __future__ import annotations

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

    def push(self, address: int):
        self.contents.append(address)

    def pop(self) -> int:
        return self.contents.pop()

    def peek(self) -> int:
        return self.contents[-1]
