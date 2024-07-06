# main.py
# the main function. When you run this file it will call system to get everything started

# imports here -- 
from system import System

# main
def main():
    _system = System()  # creates an instance of system -- calls constructor
    _system.startSystem() # after building the system -- call start system

    # get file name and call down to memory to attempt to load it
    try:
        fileName = input("Enter ROM file path: ")
        print(fileName)
        _system.loadROM(fileName)
    except:
        print("There was an issue when attempting to load in the ROM...")

    _system.cycle(True) # start the cpu cycle

if __name__ == "__main__":
    main()

    