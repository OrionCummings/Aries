from CPU import CPU
from Program import Program
from pynput.keyboard import Key, Listener

P: Program = Program("Simple.aria")
C: CPU = CPU(128)
C.LoadProgram(P)

def Press(key) -> bool:
    if key == Key.space:
        C.Clock()
        C.Print()
    else:
        return False

def Main():
    
    print("Press space to execute one clock cycle")
    C.Print()  
    with Listener(on_press = Press) as L: L.join()

if __name__ == "__main__":
    Main()