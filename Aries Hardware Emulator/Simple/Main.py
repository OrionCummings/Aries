from CPU import CPU
from pynput.keyboard import Key, Listener

C: CPU = CPU()

def Press(key) -> bool:
    if key == Key.space:
        C.Clock()
        C.Print()
    else:
        return False

def Main():
    
    with Listener(on_press = Press) as L: L.join()

if __name__ == "__main__":
    Main()