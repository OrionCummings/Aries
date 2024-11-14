from Constants import PC_INC

class ProgramCounter():
    
    def __init__(Self):
        Self.Value: int = 0
    
    def __str__(Self) -> str:
        return str(Self.Value)
    
    def __eq__(Self, Value):
        return Value == Self.Value
    
    def Increment(Self):
        Self.Value += PC_INC
    
    def Set(Self, Value: int):
        Self.Value = Value