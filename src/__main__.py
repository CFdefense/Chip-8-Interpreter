# main.py
# the main function. When you run this file it will call system to get everything started

# imports here -- 
from system import System

# main
def main():
    _system = System()  # creates an instance of system -- calls constructor
    _system.startSystem() # after building the system -- call start system

    # get file name and call down to memory to attempt to load it
    fileName = input("Enter ROM File Path")
    print(fileName)
    _system.loadROM(fileName)

if __name__ == "__main__":
    main()

    