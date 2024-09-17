# ♈ Aries

The Aries Project encompasses four components: the Aries Programming Language, the Aries Assembly Language, the Aries Hardware Emulator, and the Aries Computer.

## Active Development
- Aries Programming Language

## Planned Development
- Aries Assembly Language
- Aries Hardware Emulator
- Aries Hardware Design Package

---

## The Aries Programming Language


---
## The Aries Assembly Language


---
## The Aries Hardware Emulator


---
## The Aries Computer
* 16-bit architecture
* Little endian
* Variable clock speed [1 - 10k Hz]
* 13 16-bit registers
    - 9 general purpose 16-bit Registers
        + 4 8-bit High/Low Split Registers
        + 4 16-bit registers
        + 1 bit-addressable register
    - 1 8-bit flag register
    - 16-bit stack pointer
    - 16-bit base pointer
    - 16-bit instruction pointer
* 9 flags (one 8-bit register)
    - ZF: Zero 
    - CF: Carry
    - PF: Parity
    - SF: Sign
    - OF: Overflow
    - IF: Interrupt
    - IDF: Interrupt disable
    - TF: Trap
    - HF: HPC
* 4-bit memory alignment
* 16-bit floating point number support
![The memory layout of the Aries CPU](https://github.com/OrionCummings/Aries/blob/main/Resources/GitHub/memory-map.png?raw=true)
