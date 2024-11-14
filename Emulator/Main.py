from CPU import CPU
from pynput.keyboard import Key, Listener
from Assembler import Assembler

A: Assembler = Assembler("Example.aria")
C: CPU = CPU(128, 128)
C.LoadProgram(A)

def Press(key) -> bool:
    """Runs one clock cycle if the space bar is pressed.
    Runs many clock cycles if the space bar is held."""

    if key == Key.space:
        C.Clock()
        C.Print()
        return True #?
    else:
        return False

def Main():
    
    print("Press space to execute one clock cycle")
    C.Print()  
    with Listener(on_press = Press) as L: L.join()

if __name__ == "__main__":
    Main()