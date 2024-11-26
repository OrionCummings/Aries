from CPU import CPU
from pynput.keyboard import Key, Listener
from Assembler import Assembler, AssemblerSettings, PrintMode

Settings = AssemblerSettings()
Settings.PrintMode = PrintMode.Hex
Settings.SelfTest = True

A: Assembler = Assembler("Example.aria", Settings)
C: CPU = CPU(InstructionMemorySize=16, DataMemorySize=64)
C.LoadProgram(A.Instructions, A.FileName, 0)

def Press(key) -> bool:
    """Runs one clock cycle if the space bar is pressed.
    Runs many clock cycles if the space bar is held.""" 

    if key == Key.space:
        Clock = C.Clock()
        C.Print()
        return Clock #?
    else:
        return False 

def Main():
    
    print("Press space to execute one clock cycle")
    C.Print()  
    with Listener(on_press = Press) as L: L.join()

if __name__ == "__main__":
    Main()