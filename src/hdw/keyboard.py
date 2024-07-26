# keyboard.py
# the chip-8s keyboard

# imports here -- 
import pygame   # import pygame to monitor keypad events

# keyboard
class Keyboard():

    # chip-8 keyboard constructor
    def __init__(self):
        print("Keyboard was created successfully...")
        pygame.init()   # init pygame
        self.keyPressed = None  # what key was pressed?
        self.endProgram = False   # keeps track of user ending the program
        self.keyboard = bytearray(16) # keeps track of our key status'
        self.keyMap = { # python dictionary to map key hex indices to the chip-8 keypad layout
            pygame.K_0: 0x0, pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3,
            pygame.K_4: 0x4, pygame.K_5: 0x5, pygame.K_6: 0x6, pygame.K_7: 0x7,
            pygame.K_8: 0x8, pygame.K_9: 0x9, pygame.K_a: 0xA, pygame.K_b: 0xB,
            pygame.K_c: 0xC, pygame.K_d: 0xD, pygame.K_e: 0xE, pygame.K_f: 0xF,
        }

    # return the pressed key
    def getKey(self):
        return self.keyPressed  # returns the pressed key

    # wait for keyboard input
    def waitForKeyPress(self):  # would this be a while true loop to continuosly look until done????
        pygame.event.set_allowed(pygame.KEYDOWN) # restrict event processing
        key = None # initialize flag
        
        # wait for keydown and find the associated key
        while(key == None):
            event = pygame.event.wait()
            key = self.keyMap.get(event.key)

        pygame.event.set_blocked(None) # reset event blocking

        return key


    # continuosly check for keyboard input events
    def checkKeyboardEvents(self):
        for event in pygame.event.get():
            # if the event is keyboard down input
            if event.type == pygame.KEYDOWN:
                print("Key down:" + str(event.key))
                chip8Key = self.keyMap.get(event.key)
                print("Chip-8 Key pressed " + str(chip8Key))
                if chip8Key:
                    self.keyboard[chip8Key] = 1
            # if the event is a keyboard up input
            elif event.type == pygame.KEYUP:
                chip8Key = self.keyMap.get(event.key)
                if chip8Key:
                    self.keyboard[chip8Key] = 0


    # reset the keys pressed to make sure loops function properly
    def resetKeys(self):
        self.keyPressed = None

    # Method to take in a key value and return its state
    def checkKey(self, keyValue):
        return self.keyboard[keyValue]
    
    def updateKey(self, keyValue, status):
        self.keyboard[keyValue] = status