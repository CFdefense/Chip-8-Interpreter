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
        self.keyMap = { # python dictionary to map key hex indices to the chip-8 keypad layout
            0x0: pygame.K_1, 0x1: pygame.K_2, 0x2: pygame.K_3, 0x3: pygame.K_4, 
            0x4: pygame.K_q, 0x5: pygame.K_w, 0x6: pygame.K_e, 0x7: pygame.K_r, 
            0x8: pygame.K_a, 0x9: pygame.K_s, 0xA: pygame.K_d, 0xB: pygame.K_f, 
            0xC: pygame.K_z, 0xD: pygame.K_x, 0xE: pygame.K_c, 0xF: pygame.K_v
        }

    # return the pressed key
    def getKey(self):
        return self.keyPressed  # returns the pressed key

    # wait for keyboard input
    def waitForKeyPress(self):  # would this be a while true loop to continuosly look until done????
        # loop event until event type == keydown
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.keyPressed = self.keyMap.get(event.key)
                    break


    # continuosly check for keyboard input events
    def checkForEvents(self):
        for event in pygame.event.get():
            # if the event is QUIT. set the end program variable to true
            if event.type == pygame.QUIT:
                self.endProgram = True
            # if the event is keyboard input check the key map
            if event.type == pygame.KEYDOWN:
                self.keyPressed = self.keyMap.get(event.key)


    # reset the keys pressed to make sure loops function properly
    def resetKeys(self):
        self.keyPressed = None


    #skipNextInstruction_ExA1

    #skipNextInstruction_Ex9E

    #waitForKeyPress_Fx0A