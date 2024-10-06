from returns.result import Result, Success, Failure
from AST import AST

class Generator():
    """An assembly generator."""
    
    def __init__(Self, A: AST, Target: str):
        Self.SupportedTargets = ["x86", "Aries"]
        
        if not Target in Self.SupportedTargets:
            print("Unsupported target '{}' provided!\nOnly the following targets are supported: {}\nUsing '{}' as the default target.".format(Target, Self.SupportedTargets, Self.SupportedTargets[0]))
        
        pass
    
    def Generate(Self):
        pass