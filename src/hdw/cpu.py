# cpu.py
# the chip-8s cpu

# imports here --
from hdw.memory import Memory

# cpu
class Cpu():

    # chip-8 cpu constructor
    def __init__(self, memory):
        print("CPU was created successfully...")
        self._memory = memory   # pass in memory so the cpu is aware of it
        self.registers = bytearray(16)  # 16 8-bit registers
        self.stack = bytearray(16)  # keeps track of subroutines and order of execution
        self.programCounter = 0x200 # 16-bit program counter -- holds address of next instruction
        self.stackPointer = 0x52   #  8-bit int that points to location within the stack
        self.indexRegister = 0  # 16-bit memory address pointer
        self.delayTimer = 0 # this timer does nothing more than subtract 1 from the value of DT at a rate of 60Hz
        # self.timerHalted = False # determines if the delay timer is active
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
            self.soundTimer -= 1

    # increments the program counter by 2 for the next instruction
    def incrementPC(self):
        self.programCounter += 2    # increment after execute
        
    # step through each instruction
    def step(self):
        self.opCode = self.fetch()  # call fetch
        self.incrementPC()  # increment the program counter
        self.instruction = self.decode()    # call decode
        self.execute()  # call execute

    # fetches the HOB and LOB from memory
    def fetch(self):
        return self.combineBytes(self._memory.generalMemory[self.programCounter], self._memory.generalMemory[self.programCounter + 1])

    # combine the bytes from memory in big endian format
    def combineBytes(self, LOB, HOB):
        return (HOB << 8 | LOB)

    # opcode -> instruction
    def decode(self):
        return (hex(self.opCode))
    
    # execute the correct operation based off of the current instruction
    def execute(self):
        print(self.instruction, end= " ")

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
        print("implement clear screen")

    # return from a subroutine -- RET/00EE
    def returnSub_00EE(self):
        self.programCounter = self.stack[self.stackPointer]
        self.stackPointer -= 1

    # jumps to a machine code routine at address nnn
    def jump2MachineCodeRoutine_0nnn(self):
        print("not implemented yet")

    # jump to address nnn -- JP addr/1nnn
    def jumpAddr_1nnn(self):
        address = self.opCode & 0x0FFF  # extract lower 12 bits
        self.programCounter = address   # set program counter to the address

    # call a subroutine at nnn -- CALL addr/2nnn
    def callAddr_2nnn(self):
        address = self.opCode & 0x0FFF  # extract lower 12 bits
        self.stackPointer += 1
        self.stack[self.stackPointer] = self.programCounter
        self.programCounter = address

    # skip the next instruction if Vx == kk
    def skipNextInstruction_3xkk(self):
        # compare register Vx to kk
        Vx = (self.opCode & 0x0F00) >> 8    # Extract x nibble -> 0x3'x'kk
        kk = self.opCode & 0x00FF    # grab last byte by masking -> No need to shift 

        if(self.registers[Vx] == kk):
            self.incrementPC()

    # skip the next instruction if Vx != kk
    def skipNextInstruction_4xkk(self):
        # compare register Vx to kk
        Vx = (self.opCode & 0x0F00) >> 8    # wxtract x nibble -> 0x4'x'kk
        kk = self.opCode & 0x00FF    # grab last byte by masking

        if(self.registers[Vx] != kk):
            self.incrementPC()

    # skip the next instruction if Vx == Vy
    def skipNextInstruction_5xy0(self):
        # compare registers Vx and Vy
        Vx = (self.opCode & 0x0F00) >> 8    # mask x and shift bits
        Vy = (self.opCode & 0x00F0) >> 4     # mask y and shift bits

        if(self.registers[Vx] == self.registers[Vy]):
            self.incrementPC()

    # set the register Vx = kk
    def setRegisterVx_6xkk(self):
        # set register Vx to kk
        Vx = (self.opCode & 0x0F00) >> 8    # mask x and shift bits
        kk = self.opCode & 0x00FF    # grab last byte by masking

        self.registers[Vx] = kk

    # set the register Vx = Vx + kk
    def setRegisterVx_7xkk(self):
        # set register Vx to Vx + kk
        Vx = (self.opCode & 0x0F00) >> 8    # mask x and shift bits
        kk = self.opCode & 0x00FF    # grab last byte by masking

        self.registers[Vx] += kk

    # set the register Vx = Vy
    def setRegisterVx_8xy0(self):
        # set register Vx = Vy
        Vx = (self.opCode & 0x0F00) >> 8    # mask x and shift bits
        Vy = (self.opCode & 0x00F0) >> 4     # mask y and shift bits

        self.registers[Vx] = self.registers[Vy]

    # set the register Vx = Vx OR Vy
    def setRegisterVx_8xy1(self):
        Vx = (self.opCode & 0x0F00) >> 8 # mask x and shift bits
        Vy = (self.opCode & 0x00F0) >> 4 # mask y and shift bits

        # perform and store OR on Vx and Vy
        self.registers[Vx] |= self.registers[Vy]

    # set the register Vx = Vx AND Vy
    def setRegisterVx_8xy2(self):
        Vx = (self.opCode & 0x0F00) >> 8 # mask x and shift bits
        Vy = (self.opCode & 0x00F0) >> 4 # mask y and shift bits

        # perform and store AND on Vx and Vy
        self.registers[Vx] &= self.registers[Vy]

    # set the register Vx = Vx XOR Vy
    def setRegisterVx_8xy3(self):
        Vx = (self.opCode & 0x0F00) >> 8 # mask x and shift bits
        Vy = (self.opCode & 0x00F0) >> 4 # mask y and shift bits

        # perform and store XOR on Vx and Vy
        self.registers[Vx] ^= self.registers[Vy]

    # set the register Vx = Vx + Vy, and set VF = carry
    def setRegisterVx_8xy4(self):
        Vx = (self.opCode & 0x0F00) >> 8 # mask x and shift bits
        Vy = (self.opCode & 0x00F0) >> 4 # mask y and shift bits

        # check if > 255
        if(self.registers[Vx] + self.registers[Vy] > 0xFF):
            self.registers[0xF] = 1 # VF Takes 1
        else:
            self.registers[0xF] = 0 # VF Takes 0

        # mask and store lowest byte
        self.registers[Vx] = (self.registers[Vx] + self.registers[Vy]) & 0xFF

    # set the register Vx = Vx - Vy, and set VF = NOT borrow
    def setRegisterVx_8xy5(self):
        Vx = (self.opCode & 0x0F00) >> 8 # mask x and shift bits
        Vy = (self.opCode & 0x00F0) >> 4 # mask y and shift bits

        if(self.registers[Vx] > self.registers[Vy]):
            self.registers[0xF] = 1 # VF Takes 1
        else:
            self.registers[0xF] = 0 # VF Takes 0

        # Vy subtracted and stored in Vx
        self.registers[Vx] -= self.registers[Vy]

    # set the register Vx = Vx SHR 1
    def setRegisterVx_8xy6(self):
        Vx = (self.opCode & 0x0F00) >> 8 # mask x and shift bits

        # check if LSB is 1
        if(self.registers[Vx] & 0x1 == 1):
            self.registers[0xF] = 1 # VF Set to 1
        else:
            self.registers[0xF] = 0 # VF Set to 0

        # Vx shifted right by 1 AKA divided by two
        self.registers[Vx] >>= 1

    # set the register Vx = Vy - Vx, and set VF = NOT borrow
    def setRegisterVx_8xy7(self):
        Vx = (self.opCode & 0x0F00) >> 8 # mask x and shift bits
        Vy = (self.opCode & 0x00F0) >> 4 # mask y and shift bits

        if(self.registers[Vy] > self.registers[Vx]):
            self.registers[0xF] = 1 # VF Set to 1
        else:
            self.registers[0xF] = 0 # VF Set to 0
        
        # Vx subtracted FROM Vy and Stored in Vx
        self.registers[Vx] = self.registers[Vy] - self.registers[Vx]

    # set the register Vx = Vx SHL 1
    def setRegisterVx_8xyE(self):
        Vx = (self.opCode & 0x0F00) >> 8 # mask x and shift bits

        # check if MSB is 1
        if(self.registers[Vx] & 0x80 == 1):
            self.registers[0xF] = 1 # VF Set to 1
        else:
            self.registers[0xF] = 0 # VF Set to 0

        # Vx shifted left by 1 AKA multiplied by two
        self.registers[Vx] <<= 1

    # skip the next instruction if Vx != Vy
    def skipNextInstruction_9xy0(self):
        Vx = (self.opCode & 0x0F00) >> 8 # mask x and shift bits
        Vy = (self.opCode & 0x00F0) >> 4 # mask y and shift bits

        # if they are not equal PC += 2
        if(self.registers[Vx] != self.registers[Vy]):
            self.incrementPC()

    # set the register I = nnn
    def setRegisterI_Annn(self):
        nnn = (self.opCode & 0x0FFF) # mask last 12 bits

        # nnn stored in index register
        self.indexRegister = nnn

    # jump to location nnn + V0
    def jump2Location_Bnnn(self):
        nnn = (self.opCode & 0x0FFF) # mask last 12 bits

        # PC is set to nnn + V0
        self.programCounter = nnn + self.registers[0] 
        

    # set the register Vx = random byte AND kk.
    def setRegisterVx_Cxkk(self):
        print("test...") # develop randomizer

    # display sprite starting at memory location I
    def displaySprite_Dxyn(self):
        print("Implement Monitor")

    # skip the next instruction if a key with the value of Vx is pressed
    def skipNextInstruction_Ex9E(self):
        print("Implement Keyboard")

    # skip the next instruction if a key with the value of Vx is not pressed
    def skipNextInstruction_ExA1(self):
        print("Implement Keyboard")

    # set the register Vx = delay timer
    def setRegisterVx_Fx07(self):
        Vx = (self.opCode & 0x0F00) >> 8 # Mask x and shift bits

        # place DT Value into Vx
        self.register[Vx] = self.delayTimer

    # wait for a key press and store the value of the key in the register Vx
    def waitForKeyPress_Fx0A(self):
        print("Implement Keyboard")

    # set the delay timer = Vx
    def setDelayTimer_Fx15(self):
        Vx = (self.opCode & 0x0F00) >> 8 # Mask x and shift bits

        # set timer equal to Vx
        self.delayTimer = self.registers[Vx]

    # set the sound timer = Vx
    def setSoundTimer_Fx18(self):
        Vx = (self.opCode & 0x0F00) >> 8 # Mask x and shift bits

        # set timer equal to Vx
        self.soundTimer = self.registers[Vx]

    # set the register I = I + Vx
    def setRegisterI_Fx1E(self):
        Vx = (self.opCode & 0x0F00) >> 8 # Mask x and shift bits

        # set Index to index add Vx
        self.indexRegister += self.registers[Vx]

    # set the register I = location of a sprite for digit Vx
    def setRegisterI_Fx29(self):
        print("Implement some talk to memory sprites")

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

    # store registers in memory
    def storeRegistersInMemory_Fx55(self):
        Vx = (self.opCode & 0x0F00) >> 8  # Mask x and shift bits

        # iterate through registers V0 to Vx
        for i in range(self.registers[Vx] + 1):
            # store Register Value into Memory Starting at Index Register
            self.memory.addToMemory(self.indexRegister + i, self.registers[i])

    # read registers from memory
    def readRegisters_Fx65(self):
        Vx = (self.opCode & 0x0F00) >> 8  # Mask x and shift bits

        # iterate through Registers
        for i in range(self.registers[Vx] + 1):
            # Add from Memory Starting at Index Register
            self.registers[i] = self._memory.getFromMemory(self.indexRegister + i)