# cpu.py
# the chip-8s cpu

# imports here --

# cpu
class Cpu():

    # chip-8 cpu constructor
    def __init__(self):
        print("CPU was created successfully...")
        self.registers = bytearray(16)  # 16 8-bit registers
        self.stack = bytearray(16)  # keeps track of subroutines and order of execution
        self.programCounter # 16-bit program counter -- holds address of next instruction
        self.stackPointer   #  8-bit int that points to location within the stack
        self.indexRegister  # 16-bit memory address pointer
        self.delayTimer # this timer does nothing more than subtract 1 from the value of DT at a rate of 60Hz
        self.soundTimer # this timer also decrements at a rate of 60Hz, however, as long as ST's value is greater than zero, the Chip-8 buzzer will sound
        self.opCode


    # combine the bytes from memory in big endian format
    def combineBytes(self, HOB, LOB):

    # fetches instruction from memory
    def fetch(self):

    def decode(self):
    
    def execute(self):