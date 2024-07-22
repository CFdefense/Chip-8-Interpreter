

class Keyboard():

    def __init__(self):
        print("Keyboard was created successfully...")
        self.keys = [False] * 16 # keypad/keyboard that stores the current state of a key. Size 16