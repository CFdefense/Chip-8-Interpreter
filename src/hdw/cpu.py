# cpu.py
# the chip-8s cpu

# imports here --
from hdw.memory import Memory

# cpu
class Cpu():

    # chip-8 cpu constructor
    def __init__(self, memory):
        print("CPU was created successfully...")
        self._memory = memory   # pass in memory so the cpu is aware of it
        self.registers = bytearray(16)  # 16 8-bit registers
        self.stack = bytearray(16)  # keeps track of subroutines and order of execution
        self.programCounter = 0x200 # 16-bit program counter -- holds address of next instruction
        self.stackPointer = 0x52   #  8-bit int that points to location within the stack
        self.indexRegister = 0  # 16-bit memory address pointer
        self.delayTimer = 0 # this timer does nothing more than subtract 1 from the value of DT at a rate of 60Hz
        self.soundTimer = 0 # this timer also decrements at a rate of 60Hz, however, as long as ST's value is greater than zero, the Chip-8 buzzer will sound
        self.opCode = 0 # the current op code
        self.instruction = 0    # the current instruction

    # cpu cycle
    def cycle(self, status):
        self.step()

    # combine the bytes from memory in big endian format
    def combineBytes(self, LOB, HOB):
        return (HOB << 8 | LOB)

    # step through each instruction
    def step(self):
        self.opCode = self.fetch()  # call fetch
        self.programCounter += 2
        self.instruction = self.decode()    # call decode
        self.execute()  # call execute

    # fetches the HOB and LOB from memory
    def fetch(self):
        return self.combineBytes(self._memory.generalMemory[self.programCounter], self._memory.generalMemory[self.programCounter + 1])

    # opcode -> instruction
    def decode(self):
        print(hex(self.opCode))
        return 0
    
    # execute the correct operation based off of the current instruction
    def execute(self):
        print(self.instruction)