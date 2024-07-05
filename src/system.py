# system.py
# the entire system and the primary file for everything

# imports here -- 
from hdw.memory import Memory

# system
class System():

    # chip-8 system constructor
    def __init__(self):
        self._memory = Memory()
        # add more component initilization below

    # starts the entire system
    def startSystem(self):
        print("System started successfully...")

    # calls load function memory
    def loadROM(self, fileName):
        self._memory.loadProgramIntoMemory(fileName)
        self._memory.dumpMemory(0, 800)
