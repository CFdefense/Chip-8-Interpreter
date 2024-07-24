# monitor.py
# chip-8 uses a 64x32 monochrome (black or white) display


import pygame # For Monitor Rendering -> Maybe Change if Using Website

# monitor
class Monitor():

    # chip-8 monitor constructor
    def __init__(self):
        print("Monitor was successfully created...")
        self.width = 64
        self.height = 32
        self.scale = 10 # can be adjusted
        self.display = [0] * (self.width * self.height)
        pygame.init()
        self.window = pygame.display.set_mode((self.width * self.scale, self.height * self.scale))
        pygame.display.set_caption("Chip-8 Emulator")

    # update display render whenever we modify the display
    def updateRender(self):
        self.window.fill((0,0,0)) # wipe the screen
        for x in range(self.width): # for each y
            for y in range(self.height): # for each x
                if self.display[x + (y * self.width)] == 1:  # if it is active
                    # draw white rectangle
                    pygame.draw.rect(self.window, (255, 255, 255), (x * self.scale, y * self.scale, self.scale, self.scale))
        pygame.display.flip() # update display

    # check if window is closed
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Display window closed")
                pygame.quit()
                exit()

    # act on clearScreen_00E0 instruction
    def clearDisplay(self):
        for i in range(len(self.display)):
            self.display[i] = 0
        self.updateRender()  # Update the display rendering after clearing

    # act on displaySprite_Dxyn instruction
    def displaySprite(self, x, y, spriteList, numbytes):
        isCollision = 0 # our collision flag to be returned and updated by cpu
        for n in range(numbytes): # for number of bytes
            pixel = spriteList[n] # get current byte
            for xCor in range(8): # for bit in byte
                if(pixel & (0x80 >> xCor)) != 0: # check if bit is not set 
                    drawIndex = (x + xCor + ((y + n) * self.width)) % (self.width * self.height) # calculate index to draw pixel
                    if self.display[drawIndex] == 1: # check for collision at index of pixel
                        isCollision = 1 # upd collision flag
                    self.display[drawIndex] ^= 1  # XOR index to update pixel
        self.updateRender() # call method to update the display

        # return collision flag to be stored in VF
        return isCollision
