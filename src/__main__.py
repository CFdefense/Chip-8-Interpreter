# main.py
# the main function. When you run this file it will call system to get verything started

# imports here -- 
from system import System

# main
def main():
    _system = System()  # creates an instance of system -- calls constructor
    _system.startSystem() # after building the system -- call start system


if __name__ == "__main__":
    main()

    