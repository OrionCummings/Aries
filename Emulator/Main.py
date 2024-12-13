from CPU import CPU
from pynput.keyboard import Key, Listener
from Assembler import Assembler, AssemblerSettings, PrintMode
from PrettyPrinting import PP

settings = AssemblerSettings()
settings.print_mode = PrintMode.Hex
settings.self_test = False

a = Assembler("Example.aria", settings)
c = CPU(instruction_memory_size=16, data_memory_size=64)
c.load_program(a.instructions, a.file_name, 0)

def press(key) -> bool:
    """Runs one clock cycle if the space bar is pressed.
    Runs many clock cycles if the space bar is held.""" 

    if key == Key.space:
        clock = c.clock()
        print(c)
        return clock #?
    else:
        return False 

def main():
    
    print("Press space to execute one clock cycle")
    print(c) 
    with Listener(on_press = press) as l: l.join()
    print(PP.red_bold("CPU halted"))

if __name__ == "__main__":
    main()