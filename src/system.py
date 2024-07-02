# system.py
# the entire system and the primary file for everything

# imports here -- 
from hdw.memory import Memory

# system
class System():

    # chip-8 system constructor
    def __init__(self):
        self._memory = Memory()

    # starts the entire system
    def startSystem(self):
        print("Done!")
