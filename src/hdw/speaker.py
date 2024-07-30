# speaker.py
# chip-8 requires a speaker for sound effects

import pygame # for interacting with established pygame instance -> change if online?
import os # for reading file

# speaker
class Speaker():

    # constructor
    def __init__(self):
        print("Speaker was successfully created...")
        pygame.mixer.init() # init pygame use of sounds
        self.soundEffect = pygame.mixer.Sound(os.path.join("sounds","699927__8bitmyketison__grunt-01-retro-lo-fi.wav"))

    # to play sound effect
    def playSound(self):
        pygame.mixer.Sound.play(self.soundEffect)