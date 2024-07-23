# memory.py
# the chip-8's memory
#IMPORTANT CONTEXT -> 0x000 to 0x1FF (0 to 511) Reserved for Interpreter,
# 0x200 (512) and above for storing ROMS

# imports here ---

# memory
class Memory():

    # chip-8 memory constructor
    def __init__(self):
        print("Memory was created successfully...")
        self.generalMemory = bytearray(4096) # general memory 4096 bytes (4kb)
        self.initSprites()  # call function to init sprites array
        self.loadSprites()  # call function to load all of the sprites into memory
    
    # load sprites into sprite array
    def initSprites(self):
        # array holding the 16, 5 bytes sprites
        self.sprites = bytearray([
            0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
            0x90, 0x90, 0xF0, 0x10, 0x10, # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
            0xF0, 0x10, 0x20, 0x40, 0x40, # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90, # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
            0xF0, 0x80, 0x80, 0x80, 0xF0, # C
            0xE0, 0x90, 0x90, 0x90, 0xE0, # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
            0xF0, 0x80, 0xF0, 0x80, 0x80  # F
        ])
    
    # load the sprites from the sprites array into general memory
    def loadSprites(self):
        for i in range(len(self.sprites)):
            self.generalMemory[i] = self.sprites[i]

    # load a program into general memory
    def loadProgramIntoMemory(self, fileName):
        startingMem = 0x200 # chip-8 programs start at 0x200

        # open file and read in the content
        with open(fileName, 'rb') as romFile:
            romContents = romFile.read()

            # check if the loaded ROM is too big
            if(len(romContents) > len(self.generalMemory) - startingMem):
                print("ROM Exceeded Remaining Memory Space")
            else:
                # load ROM into General memory after 0x200 (512)
                for i, final in enumerate(romContents):
                    self.generalMemory[startingMem + i] = final
            
    # dumps the memory from one location to another
    def dumpMemory(self, start, end):
        print("Dumping Memory...")
        
        # dump mem
        for i in range(start, end):
            print(hex(self.generalMemory[i]) + " @ " + str(i), end=" ")

    # adds a value to a specific spot in the memory
    def addToMemory(self, location, value):
        self.generalMemory[location] = value

    # retrieve a value from memory
    def getFromMemory(self, location):
        return self.generalMemory[location]
