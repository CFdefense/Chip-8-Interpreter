# system.py
# the entire system and the primary file for everything

# imports here -- 
from hdw.memory import Memory
from hdw.cpu import Cpu
from hdw.keyboard import Keyboard
from hdw.monitor import Monitor
from hdw.speaker import Speaker

# system
class System():

    # chip-8 system constructor
    def __init__(self):
        self._memory = Memory() # the systems memory
        self._keyboard = Keyboard() # the systems keyboard 
        self._monitor = Monitor() # the systems monitor
        self._speaker = Speaker() # the systems speaker
        self._cpu = Cpu(self._memory, self._monitor, self._keyboard, self._speaker) # the systems cpu

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
        
        # some type of while loop to continuously call cycle
        while True:
            self._cpu.cycle() # start the cpu cycle

            # update when necessary and outside of cycle for responsiveness
            if(self._cpu.drawFlag):
                self._monitor.updateRender()
                self._cpu.drawFlag = False

            self._keyboard.checkKeyboardEvents() # continously check for keyboard inputs

    # calls memory and passes it the name of the ROM to load in
    def loadROM(self, fileName):
        self._memory.loadProgramIntoMemory(fileName)