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
        self.timerHalted = False # determines if the delay timer is active
        self.soundTimer = 0 # this timer also decrements at a rate of 60Hz
        self.opCode = 0 # the current op code
        self.instruction = 0    # the current instruction

    # cpu cycle
    def cycle(self):
        self.step() # step through each instruction

        # decrement the delay timer by 1 until it is 0
        if(self.delayTimer > 0):
            self.delayTimer -= 1
        else:
            self.timerHalted = True

        # decrement the sound timer by 1 while its greater than 0
        if(self.soundTimer > 0):
            self.soundTimer -= 1
        else:
            # diasble the sound timer     
            print("Not implemented yet")

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
        # built in switch cases do not exist use if-else

        # determine the instruction to execute
        if(self.opCode & 0xF000 == 0x0000):
            if(self.opCode == 0x00E0):
                self.clearScreen()
            elif(self.opCode == 0x00EE):
                self.returnSub()
            else:
                self.jump2MachineCodeRoutine()
        elif(self.opCode & 0xF000 == 0x1000):
            self.jumpAddr()
        elif(self.opCode & 0xF000 == 0x2000):
            self.callAddr()
        elif(self.opCode & 0xF000 == 0x3000):
            self.skipNextInstruction3xkk()
        elif(self.opCode & 0xF000 == 0x4000):
            self.skipNextInstruction4xkk()
        elif(self.opCode & 0xF000 == 0x5000):
            self.skipNextInstruction5xy0()
        elif(self.opCode & 0xF000 == 0x6000):
            self.setRegisterVx6xkk()
        elif(self.opCode & 0xF000 == 0x7000):
            self.setRegisterVx7xkk()
        elif(self.opCode & 0xF000 == 0x8000):
            if(self.opCode & 0x000F == 0x0000):
                self.setRegisterVx8xy0()
            elif(self.opCode & 0x000F == 0x0001):
                self.setRegisterVx8xy1()
            elif(self.opCode & 0x000F == 0x0002):
                self.setRegisterVx8xy2()
            elif(self.opCode & 0x000F == 0x0003):
                self.setRegisterVx8xy3()
            elif(self.opCode & 0x000F == 0x0004):
                self.setRegisterVx8xy4()
            elif(self.opCode & 0x000F == 0x0005):
                self.setRegisterVx8xy5()
            elif(self.opCode & 0x000F == 0x0006):
                self.setRegisterVx8xy6()
            elif(self.opCode & 0x000F == 0x0007):
                self.setRegisterVx8xy7()
            elif(self.opCode & 0x000F == 0x000E):
                self.iSHLVxVy()
        elif(self.opCode & 0xF000 == 0x9000):
            self.iSNEVxVy()
        elif(self.opCode & 0xF000 == 0xA000):
            self.iLDIndex()
        elif(self.opCode & 0xF000 == 0xB000):
            self.iJpVAddr()
        elif(self.opCode & 0xF000 == 0xC000):
            self.iSetVxRand()
        elif(self.opCode & 0xF000 == 0xD000):
            self.iDisplayBy()
        elif(self.opCode & 0xF000 == 0xE000):
            if(self.opCode & 0x000F == 0x000E):
                self.iSkipVxIs()
            elif(self.opCode & 0x000F == 0x0001):
                self.iSkipVxIsN()
        elif(self.opCode & 0xF000 == 0xF000):
            if(self.opCode & 0x000F == 0x0007):
                self.iSetVxDT()
            elif(self.opCode & 0x000F == 0x000A):
                self.iWaitKey()
            elif(self.opCode & 0x000F == 0x0008):
                self.iSetSound()
            elif(self.opCode & 0x000F == 0x000E):
                self.iSetVxI()
            elif(self.opCode & 0x000F == 0x0009):
                self.iSetISprite()
            elif(self.opCode & 0x000F == 0x0003):
                self.iStoreBCD()
            elif(self.opCode & 0x000F == 0x0005):
                if(self.opCode & 0x00F0 == 0x0010):
                    self.iSetDelay()
                elif(self.opCode & 0x00F0 == 0x0050):
                    self.iStoreV0Vx()
                elif(self.opCode & 0x00F0 == 0x0060):
                    self.iReadV0Vx()
            
    # clear the display -- CLS/00E0
    def clearScreen_00E0(self):
        print("implement clear screen")

    # return from a subroutine -- RET/00EE
    def returnSub_00EE(self):
        # decrement the stack pointer and reset the program counter
        self.stackPointer -= 1
        self.programCounter = self.stack[self.stackPointer]

    # do we need this???
    # jumps to a machine code routine at address nnn
    def jump2MachineCodeRoutine_0nnn(self):
        print("Necessary?")

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
        Vx = (self.opCode + 0x0FFF) >> 8    # shift bits
        kk = self.opCode + 0x0FFF    # grab last byte by masking

        if(self.registers[Vx] == kk):
            self.incrementPC()

    # skip the next instruction if Vx != kk
    def skipNextInstruction_4xkk(self):
        # compare register Vx to kk
        Vx = (self.opCode + 0x0FFF) >> 8    # shift bits
        kk = self.opCode + 0x0FFF    # grab last byte by masking

        if(self.registers[Vx] != kk):
            self.incrementPC()

    # skip the next instruction if Vx == Vy
    def skipNextInstruction_5xy0(self):
        # compare registers Vx and Vy
        Vx = (self.opCode + 0x0FFF) >> 8    # shift bits
        Vy = (self.opCode + 0x0FFF) >> 4     # shift bits

        if(self.registers[Vx] == self.registers[Vy]):
            self.incrementPC()

    # set the register Vx = kk
    def setRegisterVx_6xkk(self):
        # set register Vx to kk
        Vx = (self.opCode + 0x0FFF) >> 8    # shift bits
        kk = self.opCode + 0x0FFF    # grab last byte by masking

        self.registers[Vx] = kk

    # set the register Vx = Vx + kk
    def setRegisterVx_7xkk(self):
        # set register Vx to Vx + kk
        Vx = (self.opCode + 0x0FFF) >> 8    # shift bits
        kk = self.opCode + 0x0FFF    # grab last byte by masking

        self.registers[Vx] += kk

    # set the register Vx = Vy
    def setRegisterVx_8xy0(self):
        # set register Vx = Vy
        Vx = (self.opCode + 0x0FFF) >> 8    # shift bits
        Vy = (self.opCode + 0x0FFF) >> 4     # shift bits

        self.registers[Vx] = self.registers[Vy]

    def setRegisterVx_8xy1(self):
        print("test...")

    def setRegisterVx_8xy2(self):
        print("test...")

    def setRegisterVx_8xy3(self):
        print("test...")

    def setRegisterVx_8xy4(self):
        print("test...")

    def setRegisterVx_8xy5(self):
        print("test...")

    def setRegisterVx_8xy6(self):
        print("test...")

    def setRegisterVx_8xy7(self):
        print("test...")

    def setRegisterVx_8xyE(self):
        print("test...")

    def skipNextInstruction_9xy0(self):
        print("test...")

    def setRegisterI_Annn(self):
        print("test...")

    def jump2Location_Bnnn(self):
        print("test...")

    def setRegisterVx_Cxkk(self):
        print("test...")

    def displaySprite_Dxyn(self):
        print("test...")

    def skipNextInstruction_Ex9E(self):
        print("test...")

    def skipNextInstruction_ExA1(self):
        print("test...")

    def setRegisterVx_Fx07(self):
        print("test...")

    def waitForKeyPress_Fx0A(self):
        print("test...")

    def setDelayTimer_Fx15(self):
        print("test...")

    def setSoundTimer_Fx18(self):
        print("test...")

    def setRegisterI_Fx1E(self):
        print("test...")

    def setRegisterI_Fx29(self):
        print("test...")

    def storeBCDRepresentationInMemory_Fx33(self):
        print("test...")

    def storeRegistersInMemory_Fx55(self):
        print("test...")

    def readRegisters_Fx65(self):
        print("test...")