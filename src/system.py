# system.py
# the entire system and the primary file for everything

# imports here -- 
from hdw.memory import Memory
from hdw.cpu import Cpu

# system
class System():

    # chip-8 system constructor
    def __init__(self):
        self._memory = Memory() # the systems memory
        self._cpu = Cpu(self._memory)   # the systems cpu

    # starts the entire system
    def startSystem(self):
        print("System started successfully...")

    # calls load function memory
    def loadROM(self, fileName):
        self._memory.loadProgramIntoMemory(fileName)
        # uncomment to dump memory -- self._memory.dumpMemory(0, 800)
    
    def cycle(self, status):
        self._cpu.step()
