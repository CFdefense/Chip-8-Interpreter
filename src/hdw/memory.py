# memory.py
# the chip-8's memory

# imports here ---

# memory
class Memory():

    # chip-8 memory constructor
    def __init__(self):
        self.generalMemory = bytearray(4096) # general memory 4096 bytes (4kb)
        self.initSprites()  # call function to init sprites array
        self.loadSprites()  # call function to load all of the sprites into memory
        self.dumpMemory(0, 80)
    
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
    def loadProgramIntoMemory(self):
        pass


    # dumps the memory from one location to another
    def dumpMemory(self, start, end):
        print("Dumping Memory...")
        for i in range(start, end):
            print(self.generalMemory[i])

    
