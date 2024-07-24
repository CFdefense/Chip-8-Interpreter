# system.py
# the entire system and the primary file for everything

# imports here -- 
import time
from hdw.memory import Memory
from hdw.cpu import Cpu
from hdw.keyboard import Keyboard
from hdw.monitor import Monitor

# system
class System():

    # chip-8 system constructor
    def __init__(self):
        self._memory = Memory() # the systems memory
        self._keyboard = Keyboard() # the systems keyboard 
        self._monitor = Monitor() # the systems monitor
        self._cpu = Cpu(self._memory, self._monitor, self._keyboard) # the systems cpu
        self.cycleDuration = 1 / 60 # calculate 60hz
        self.systemHalted = False

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
        
        lastCycleTime = time.time() # get the current time
        
        # some type of while loop to continuously call cycle
        while not (self.systemHalted):
            self._monitor.handleEvents() # to handle window events -> prevents freezing and need to force quit
            self._keyboard.checkKeyboardEvents() # continuosly check for keyboard input
            
            # check if the user halts the system -- this would be through the keyboard
            if(self._keyboard.endProgram):
                self.systemHalted = True
                break
        
            currentTime = time.time()
            delayTime = currentTime - lastCycleTime

            # check if enough time has passed between cycles
            if(delayTime > self.cycleDuration):
                lastCycleTime = currentTime # update the last cycle
                self._cpu.cycle() # start the cpu cycle
                
            
        print("The System is powering down...")
        exit()

    # calls memory and passes it the name of the ROM to load in
    def loadROM(self, fileName):
        self._memory.loadProgramIntoMemory(fileName)