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
            pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3, pygame.K_4: 0xC,
            pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_r: 0xD,
            pygame.K_a: 0x7, pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_f: 0xE,
            pygame.K_z: 0xA, pygame.K_x: 0x0, pygame.K_c: 0xB, pygame.K_v: 0xF
        }

    # return the pressed key
    def getKey(self):
        return self.keyPressed  # returns the pressed key

    # wait for keyboard input
    def waitForKeyPress(self):
        pygame.event.set_allowed(pygame.KEYDOWN) # restrict event processing
        pygame.event.clear()
        key = None # initialize flag
        
        # wait for keydown and find the associated key
        while(key == None):
            event = pygame.event.wait()
            key = self.keyMap.get(event.key)

        pygame.event.set_blocked(None) # reset event blocking

        return key


    # continuosly check for keyboard input events
    def checkKeyboardEvents(self):
        pygame.event.pump()
        events = pygame.event.get()
        for event in events:
            # if the event is keyboard down input
            if event.type == pygame.KEYDOWN:
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