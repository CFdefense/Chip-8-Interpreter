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

        # get the ROM from the user and call memory to load it in
        try:
            fileName = input("Enter ROM file path: ")
            print(fileName)
            self.loadROM(fileName)
        # output if there is an error
        except:
            print("There was an issue when attempting to load in the ROM...")

        self._cpu.cycle(True) # start the cpu cycle

    # calls memory and passes it the name of the ROM to load in
    def loadROM(self, fileName):
        self._memory.loadProgramIntoMemory(fileName)
        # uncomment to dump memory -- self._memory.dumpMemory(0, 800)