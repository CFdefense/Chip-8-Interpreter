# keyboard.py
# the chip-8s keyboard

# imports here -- 


# keyboard
class Keyboard():

    # chip-8 keyboard constructor
    def __init__(self):
        print("Keyboard was created successfully...")
        self.keys = [False] * 16 # keypad/keyboard that stores the current state of a key. Size 16
        self.keyMap = { # python dictionary to map key hex indices to the chip-8 keypad layout
            0x0: '1', 0x1: '2', 0x2: '3', 0x3: '4',
            0x4: 'q', 0x5: 'w', 0x6: 'e', 0x7: 'r',
            0x8: 'a', 0x9: 's', 0xA: 'd', 0xB: 'f',
            0xC: 'z', 0xD: 'x', 0xE: 'c', 0xF: 'v'
        }

    #skipNextInstruction_ExA1

    #skipNextInstruction_Ex9E

    #waitForKeyPress_Fx0A