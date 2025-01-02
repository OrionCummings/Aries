from CPU import CPU
from pynput.keyboard import Key, Listener
from Assembler import Assembler, AssemblerSettings, PrintMode
from PrettyPrinting import red_bold

settings = AssemblerSettings()
settings.print_mode = PrintMode.Hex
settings.self_test = False

assembler = Assembler("Instructions/ldi.aria", settings)
cpu = CPU(instruction_memory_size=16, data_memory_size=64)
cpu.load_program(assembler.instructions, assembler.file_name, 0)

def press(key) -> bool:
    """Runs one clock cycle if the space bar is pressed.
    Runs many clock cycles if the space bar is held.""" 

    if key == Key.space:
        
        # Clear the screen
        # print("\033c", end="")
        
        # Run one clock cycle of the CPU
        clock = cpu.clock()
        
        # Print the CPU state
        print(cpu)
        
        
        return clock #?
    else:
        return False 

def main():
    
    print("Press space to execute one clock cycle")
    print(cpu) 
    with Listener(on_press = press) as l: l.join()
    print(red_bold("CPU halted"))

if __name__ == "__main__":
    main()