from Constants import PC_INC

class ProgramCounter():
    
    def __init__(self):
        self.value: int = 0
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __eq__(self, value):
        return value == self.value
    
    def increment(self):
        self.value += PC_INC
    
    def set(self, value: int):
        self.value = value