# cpu.py
# the chip-8s cpu

# imports here --
from hdw.memory import Memory
from hdw.monitor import Monitor
from hdw.keyboard import Keyboard

import random # for use in Cxkk instruction
# cpu
class Cpu():

    # chip-8 cpu constructor
    def __init__(self, memory, monitor, keyboard):
        print("CPU was created successfully...")
        self._memory = memory   # pass in memory so the cpu is aware of it
        self._monitor = monitor
        self._keyboard = keyboard
        self.registers = bytearray(16)  # 16 8-bit registers
        self.stack = [0] * 16  # keeps track of subroutines and order of execution 16 bit
        self.programCounter = 0x200 # 16-bit program counter -- holds address of next instruction
        self.stackPointer = 0   #  8-bit int that points to location within the stack
        self.indexRegister = 0  # 16-bit memory address pointer
        self.delayTimer = 0 # this timer does nothing more than subtract 1 from the value of DT at a rate of 60Hz
        self.soundTimer = 0 # this timer also decrements at a rate of 60Hz
        self.opCode = 0 # the current op code
        self.instruction = 0    # the current instruction

    # cpu cycle
    def cycle(self):
        self.step() # step through each instruction

        # decrement the delay timer by 1 until it is 0
        if(self.delayTimer > 0):
            self.delayTimer -= 1

        # decrement the sound timer by 1 while its greater than 0
        if(self.soundTimer > 0):
            if(self.soundTimer == 1):
                self.beep()
            self.soundTimer -= 1

    # increments the program counter by 2 for the next instruction
    def incrementPC(self):
        self.programCounter += 2    # increment after execute
    
    # temp method for sound timer
    def beep():
        print("beep")

    def pushToStack(self, value):
        if self.stackPointer >= len(self.stack):
            raise OverflowError("Stack overflow")
        else:
            self.stack[self.stackPointer] = value
            self.stackPointer += 1

    def popFromStack(self):
        if self.stackPointer == 0:
            raise IndexError("Stack underflow")
        else:
            self.stackPointer -= 1
            return self.stack[self.stackPointer]
        
    # step through each instruction
    def step(self):
        self.opCode = self.fetch()  # call fetch
        self.instruction = self.decode()    # call decode
        self.execute()  # call execute

    # fetches the HOB and LOB from memory and combines them
    def fetch(self):
        lob = (self._memory.generalMemory[self.programCounter])
        hob = (self._memory.generalMemory[self.programCounter + 1])
        return self.combinedHexBytes(hob, lob)
    
    # combine the hexidecimals
    def combinedHexBytes(self, hob, lob):
        return (lob << 8) | hob

    # opcode -> instruction
    def decode(self):
        return (hex(self.opCode))
    
    # execute the correct operation based off of the current instruction
    def execute(self):
        # print(self.instruction, end= " ")

        # determine the instruction to execute
        if(self.opCode & 0xF000 == 0x0000):
            if(self.opCode == 0x00E0):
                self.clearScreen_00E0()
            elif(self.opCode == 0x00EE):
                self.returnSub_00EE()
            else:
                self.jump2MachineCodeRoutine_0nnn()
        elif(self.opCode & 0xF000 == 0x1000):
            self.jumpAddr_1nnn()
        elif(self.opCode & 0xF000 == 0x2000):
            self.callAddr_2nnn()
        elif(self.opCode & 0xF000 == 0x3000):
            self.skipNextInstruction_3xkk()
        elif(self.opCode & 0xF000 == 0x4000):
            self.skipNextInstruction_4xkk()
        elif(self.opCode & 0xF000 == 0x5000):
            self.skipNextInstruction_5xy0()
        elif(self.opCode & 0xF000 == 0x6000):
            self.setRegisterVx_6xkk()
        elif(self.opCode & 0xF000 == 0x7000):
            self.setRegisterVx_7xkk()
        elif(self.opCode & 0xF000 == 0x8000):
            if(self.opCode & 0x000F == 0x0000):
                self.setRegisterVx_8xy0()
            elif(self.opCode & 0x000F == 0x0001):
                self.setRegisterVx_8xy1()
            elif(self.opCode & 0x000F == 0x0002):
                self.setRegisterVx_8xy2()
            elif(self.opCode & 0x000F == 0x0003):
                self.setRegisterVx_8xy3()
            elif(self.opCode & 0x000F == 0x0004):
                self.setRegisterVx_8xy4()
            elif(self.opCode & 0x000F == 0x0005):
                self.setRegisterVx_8xy5()
            elif(self.opCode & 0x000F == 0x0006):
                self.setRegisterVx_8xy6()
            elif(self.opCode & 0x000F == 0x0007):
                self.setRegisterVx_8xy7()
            elif(self.opCode & 0x000F == 0x000E):
                self.setRegisterVx_8xyE()
        elif(self.opCode & 0xF000 == 0x9000):
            self.skipNextInstruction_9xy0()
        elif(self.opCode & 0xF000 == 0xA000):
            self.setRegisterI_Annn()
        elif(self.opCode & 0xF000 == 0xB000):
            self.jump2Location_Bnnn()
        elif(self.opCode & 0xF000 == 0xC000):
            self.setRegisterVx_Cxkk()
        elif(self.opCode & 0xF000 == 0xD000):
            self.displaySprite_Dxyn()
        elif(self.opCode & 0xF000 == 0xE000):
            if(self.opCode & 0x000F == 0x000E):
                self.skipNextInstruction_Ex9E()
            elif(self.opCode & 0x000F == 0x0001):
                self.skipNextInstruction_ExA1()
        elif(self.opCode & 0xF000 == 0xF000):
            if(self.opCode & 0x000F == 0x0007):
                self.setRegisterVx_Fx07()
            elif(self.opCode & 0x000F == 0x000A):
                self.waitForKeyPress_Fx0A()
            elif(self.opCode & 0x000F == 0x0008):
                self.setSoundTimer_Fx18()
            elif(self.opCode & 0x000F == 0x000E):
                self.setRegisterI_Fx1E()
            elif(self.opCode & 0x000F == 0x0009):
                self.setRegisterI_Fx29()
            elif(self.opCode & 0x000F == 0x0003):
                self.storeBCDRepresentationInMemory_Fx33()
            elif(self.opCode & 0x000F == 0x0005):
                if(self.opCode & 0x00F0 == 0x0010):
                    self.setDelayTimer_Fx15()
                elif(self.opCode & 0x00F0 == 0x0050):
                    self.storeRegistersInMemory_Fx55()
                elif(self.opCode & 0x00F0 == 0x0060):
                    self.readRegisters_Fx65()
            
    # clear the display -- CLS/00E0
    def clearScreen_00E0(self):
        self._monitor.clearDisplay()
        self.incrementPC()  # increment the program counter

    # return from a subroutine -- RET/00EE
    def returnSub_00EE(self):
        self.programCounter = self.popFromStack() # set PC to popped

    # jumps to a machine code routine at address nnn -> not commonly used
    def jump2MachineCodeRoutine_0nnn(self):
        address = self.opCode & 0x0FFF # extract lower 12 bits
        self.programCounter = address # set program counter to the address

    # jump to address nnn -- JP addr/1nnn
    def jumpAddr_1nnn(self):
        address = self.opCode & 0x0FFF  # extract lower 12 bits
    
        self.programCounter = address # set program counter to the address
        
    # call a subroutine at nnn -- CALL addr/2nnn
    def callAddr_2nnn(self):
        # push to stack
        self.incrementPC()  # increment the program counter
        self.pushToStack(self.programCounter)
        address = self.opCode & 0x0FFF  # extract lower 12 bits
        self.programCounter = address # update pc to nibble

    # skip the next instruction if Vx == kk
    def skipNextInstruction_3xkk(self):
        # compare register Vx to kk
        Vx = (self.opCode & 0x0F00) >> 8    # Extract x nibble -> 0x3'x'kk
        kk = self.opCode & 0x00FF    # grab last byte by masking -> No need to shift 

        if(self.registers[Vx] == kk):
            self.incrementPC()
            self.incrementPC()  # increment the program counter twice to skip 
        else:
            self.incrementPC()  # increment the program counter once
        

    # skip the next instruction if Vx != kk
    def skipNextInstruction_4xkk(self):
        # compare register Vx to kk
        Vx = (self.opCode & 0x0F00) >> 8    # wxtract x nibble -> 0x4'x'kk
        kk = self.opCode & 0x00FF    # grab last byte by masking

        if(self.registers[Vx] != kk):
            self.incrementPC()
            self.incrementPC()  # increment the program counter twice
        else:
            self.incrementPC()  # increment the program counter once

    # skip the next instruction if Vx == Vy
    def skipNextInstruction_5xy0(self):
        # compare registers Vx and Vy
        Vx = (self.opCode & 0x0F00) >> 8    # mask x and shift bits
        Vy = (self.opCode & 0x00F0) >> 4     # mask y and shift bits

        if(self.registers[Vx] == self.registers[Vy]):
            self.incrementPC()
            self.incrementPC()  # increment the program counter twice
        else:
            self.incrementPC()  # increment the program counter once

    # set the register Vx = kk
    def setRegisterVx_6xkk(self):
        # set register Vx to kk
        Vx = (self.opCode & 0x0F00) >> 8    # mask x and shift bits
        kk = self.opCode & 0x00FF    # grab last byte by masking

        self.registers[Vx] = kk
        self.incrementPC()  # increment the program counter

    # set the register Vx = Vx + kk
    def setRegisterVx_7xkk(self):
        # set register Vx to Vx + kk
        Vx = (self.opCode & 0x0F00) >> 8    # mask x and shift bits
        kk = self.opCode & 0x00FF    # grab last byte by masking

        self.registers[Vx] = (self.registers[Vx] + kk) & 0xFF # Wrap Byte
        self.incrementPC()  # increment the program counter

    # set the register Vx = Vy
    def setRegisterVx_8xy0(self):
        # set register Vx = Vy
        Vx = (self.opCode & 0x0F00) >> 8    # mask x and shift bits
        Vy = (self.opCode & 0x00F0) >> 4     # mask y and shift bits

        self.registers[Vx] = self.registers[Vy]
        self.incrementPC()  # increment the program counter

    # set the register Vx = Vx OR Vy
    def setRegisterVx_8xy1(self):
        Vx = (self.opCode & 0x0F00) >> 8 # mask x and shift bits
        Vy = (self.opCode & 0x00F0) >> 4 # mask y and shift bits

        # perform and store OR on Vx and Vy
        self.registers[Vx] |= self.registers[Vy]
        self.incrementPC()  # increment the program counter

    # set the register Vx = Vx AND Vy
    def setRegisterVx_8xy2(self):
        Vx = (self.opCode & 0x0F00) >> 8 # mask x and shift bits
        Vy = (self.opCode & 0x00F0) >> 4 # mask y and shift bits

        # perform and store AND on Vx and Vy
        self.registers[Vx] &= self.registers[Vy]
        self.incrementPC()  # increment the program counter

    # set the register Vx = Vx XOR Vy
    def setRegisterVx_8xy3(self):
        Vx = (self.opCode & 0x0F00) >> 8 # mask x and shift bits
        Vy = (self.opCode & 0x00F0) >> 4 # mask y and shift bits

        # perform and store XOR on Vx and Vy
        self.registers[Vx] ^= self.registers[Vy]
        self.incrementPC()  # increment the program counter

    # set the register Vx = Vx + Vy, and set VF = carry
    def setRegisterVx_8xy4(self):
        Vx = (self.opCode & 0x0F00) >> 8 # mask x and shift bits
        Vy = (self.opCode & 0x00F0) >> 4 # mask y and shift bits

        # mask and store lowest byte
        value = self.registers[Vx] + self.registers[Vy]
        self.registers[Vx] = value & 0xFF

        # check if > 255
        if(value > 0xFF):
            self.registers[0xF] = 1 # VF Takes 1
        else:
            self.registers[0xF] = 0 # VF Takes 0

        self.incrementPC()  # increment the program counter

    # set the register Vx = Vx - Vy, and set VF = NOT borrow
    def setRegisterVx_8xy5(self):
        Vx = (self.opCode & 0x0F00) >> 8 # mask x and shift bits
        Vy = (self.opCode & 0x00F0) >> 4 # mask y and shift bits
        
        # Vy subtracted and stored in Vx
        value = self.registers[Vx] - self.registers[Vy]
        self.registers[Vx] = value & 0xFF # Wrap Byte

        if(value > 0):
            self.registers[0xF] = 1 # VF Takes 1
        else:
            self.registers[0xF] = 0 # VF Takes 0

        self.incrementPC()  # increment the program counter

    # set the register Vx = Vx SHR 1
    def setRegisterVx_8xy6(self):
        Vx = (self.opCode & 0x0F00) >> 8 # mask x and shift bits

        # check if LSB is 1
        if(self.registers[Vx] & 0x1 != 0):
            self.registers[0xF] = 1 # VF Set to 1
        else:
            self.registers[0xF] = 0 # VF Set to 0

        # Vx shifted right by 1 AKA divided by two
        self.registers[Vx] = (self.registers[Vx] >> 1) & 0xFF # Wrap Byte
        self.incrementPC()  # increment the program counter

    # set the register Vx = Vy - Vx, and set VF = NOT borrow
    def setRegisterVx_8xy7(self):
        Vx = (self.opCode & 0x0F00) >> 8 # mask x and shift bits
        Vy = (self.opCode & 0x00F0) >> 4 # mask y and shift bits

        # Vx subtracted and stored in Vx
        value = self.registers[Vy] - self.registers[Vx]
        self.registers[Vx] = value & 0xFF # Wrap Byte
        
        if(value > 0):
            self.registers[0xF] = 1 # VF Set to 1
        else:
            self.registers[0xF] = 0 # VF Set to 0
        
        self.incrementPC()  # increment the program counter

    # set the register Vx = Vx SHL 1
    def setRegisterVx_8xyE(self):
        Vx = (self.opCode & 0x0F00) >> 8 # mask x and shift bits

        # check if MSB is 1
        if(self.registers[Vx] & 0x80 != 0):
            self.registers[0xF] = 1 # VF Set to 1
        else:
            self.registers[0xF] = 0 # VF Set to 0

        # Vx shifted left by 1 AKA multiplied by two
        self.registers[Vx] = (self.registers[Vx] << 1) & 0xFF # Wrap Byte
        self.incrementPC()  # increment the program counter

    # skip the next instruction if Vx != Vy
    def skipNextInstruction_9xy0(self):
        Vx = (self.opCode & 0x0F00) >> 8 # mask x and shift bits
        Vy = (self.opCode & 0x00F0) >> 4 # mask y and shift bits

        # if they are not equal PC += 2
        if(self.registers[Vx] != self.registers[Vy]):
            self.incrementPC()
            self.incrementPC()  # increment the program counter twice
        else:
            self.incrementPC()  # increment the program counter once

    # set the register I = nnn
    def setRegisterI_Annn(self):
        nnn = (self.opCode & 0x0FFF) # mask last 12 bits

        # nnn stored in index register
        self.indexRegister = nnn
        self.incrementPC()  # increment the program counter

    # jump to location nnn + V0
    def jump2Location_Bnnn(self):
        nnn = (self.opCode & 0x0FFF) # mask last 12 bits

        # PC is set to nnn + V0
        self.programCounter = nnn + self.registers[0] 
        

    # set the register Vx = random byte AND kk.
    def setRegisterVx_Cxkk(self):
        Vx = self.opCode & 0x0F00 >> 8 # mask x and shift bits
        kk = self.opCode & 0x00FF # mask last byte

        # set Vx to random byte AND kk
        self.registers[Vx] = random.randint(0,255) & kk
        self.incrementPC()  # increment the program counter
        

    # display sprite starting at (Vx, Vy), set VF = collision.
    def displaySprite_Dxyn(self):
        Vx = (self.opCode & 0x0F00) >> 8 # mask x and shift bits -> x coordinate register
        Vy = (self.opCode & 0x00F0) >> 4 # mask y and shift bits -> y coordinate register
        nBit = self.opCode & 0x000F # mask n dont shift already at end -> num of bytes to read

        x = self.registers[Vx] # get x coordinate value
        y = self.registers[Vy] # get y coordinate value

        # read in sprite(s) from memory
        sprite = []
        for i in range(nBit):
            sprite.append(self._memory.getFromMemory(self.indexRegister + i)) # index register set earlier to be the first byte of the sprite in memory

        # Call monitor's displaySprite method
        isCollision = self._monitor.displaySprite(x, y, sprite, nBit)

        # update VF register with collision status
        self.registers[0xF] = isCollision

        self.incrementPC()  # increment the program counter

    # skip the next instruction if a key with the value of Vx is pressed
    def skipNextInstruction_Ex9E(self):
        Vx = (self.opCode & 0x0F00) >> 8 # Mask x and shift bits

        key = self.registers[Vx] # get key value from register

        # Skip the next instruction if the key is pressed
        if(self._keyboard.checkKey(key)):
            self.incrementPC()
            self.incrementPC()  # increment the program counter twice
        else:
            self.incrementPC()  # increment the program counter once

    # skip the next instruction if a key with the value of Vx is not pressed
    def skipNextInstruction_ExA1(self):
        Vx = (self.opCode & 0x0F00) >> 8 # Mask x and shift bits

        key = self.registers[Vx] # get key value from register

        # Skip the next instruction if the key is not pressed
        if not (self._keyboard.checkKey(key)):
            self.incrementPC()
            self.incrementPC()  # increment the program counter twice
        else:
            self.incrementPC()  # increment the program counter once

    # set the register Vx = delay timer
    def setRegisterVx_Fx07(self):
        Vx = (self.opCode & 0x0F00) >> 8 # Mask x and shift bits

        # place DT Value into Vx
        self.registers[Vx] = self.delayTimer
        self.incrementPC()  # increment the program counter

    # wait for a key press and store the value of the key in the register Vx
    def waitForKeyPress_Fx0A(self):
        Vx = (self.opCode & 0x0F00) >> 8  # Mask x and shift bits
        pressedKey = self._keyboard.waitForKeyPress()
        self._keyboard.updateKey(pressedKey, True)

        self.registers[Vx] = pressedKey  # Store the pressed key value in register Vx
        self.incrementPC()  # increment the program counter

    # set the delay timer = Vx
    def setDelayTimer_Fx15(self):
        Vx = (self.opCode & 0x0F00) >> 8 # Mask x and shift bits

        # set timer equal to Vx
        self.delayTimer = self.registers[Vx]
        self.incrementPC()  # increment the program counter

    # set the sound timer = Vx
    def setSoundTimer_Fx18(self):
        Vx = (self.opCode & 0x0F00) >> 8 # Mask x and shift bits

        # set timer equal to Vx
        self.soundTimer = self.registers[Vx]
        self.incrementPC()  # increment the program counter

    # set the register I = I + Vx
    def setRegisterI_Fx1E(self):
        Vx = (self.opCode & 0x0F00) >> 8 # Mask x and shift bits

        # set Index to index add Vx
        self.indexRegister += self.registers[Vx]
        self.incrementPC()  # increment the program counter

    # set the register I = location of a sprite for digit Vx
    def setRegisterI_Fx29(self):
        Vx = (self.opCode & 0x0F00) >> 8 # Mask x and shift bits

        digit = self.registers[Vx] # get digit value

        self.indexRegister = digit * 5 # each byte is stored in the memory starting at itself * 5
        self.incrementPC()  # increment the program counter

    # store a BCD representation of Vx in memory
    def storeBCDRepresentationInMemory_Fx33(self):
        Vx = (self.opCode & 0x0F00) >> 8  # Mask x and shift bits
        registerValue = self.registers[Vx]

        # calculate each decimal place
        hundredsPlace = registerValue // 100
        tensPlace = (registerValue // 10) % 10
        onesPlace = registerValue % 10

        # store the digits in memory 
        self._memory.addToMemory(self.indexRegister, hundredsPlace)
        self._memory.addToMemory(self.indexRegister + 1, tensPlace)
        self._memory.addToMemory(self.indexRegister + 2, onesPlace)
        self.incrementPC()  # increment the program counter

    # store registers in memory
    def storeRegistersInMemory_Fx55(self):
        Vx = (self.opCode & 0x0F00) >> 8  # Mask x and shift bits

        for i in range(Vx + 1): # Iterate up to and including Vx
            # store Register Value into Memory Starting at Index Register
            self._memory.addToMemory(self.indexRegister + i, self.registers[i])
        self.incrementPC()  # increment the program counter

    # read registers from memory
    def readRegisters_Fx65(self):
        Vx = (self.opCode & 0x0F00) >> 8  # Mask x and shift bits

        for i in range(Vx + 1): # Iterate up to and including Vx
            # Add from Memory Starting at Index Register
            self.registers[i] = self._memory.getFromMemory(self.indexRegister + i)
        self.incrementPC()  # increment the program counter