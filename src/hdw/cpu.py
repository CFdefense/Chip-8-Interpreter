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
        self.soundTimer = 0 # this timer also decrements at a rate of 60Hz, however, as long as ST's value is greater than zero, the Chip-8 buzzer will sound
        self.opCode = 0 # the current op code
        self.instruction = 0    # the current instruction

    # cpu cycle
    def cycle(self, status):
        # Some timer function has to be implemented here in the future to control how often step is called
            if(status == True):
                self.step()
        
    # step through each instruction
    def step(self):
        self.opCode = self.fetch()  # call fetch
        self.instruction = self.decode()    # call decode
        self.execute()  # call execute
        self.programCounter += 2    # increment after execute

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

        # Determine Instruction to Execute
        if(self.opCode & 0xF000 == 0x0000):
            if(self.opCode == 0x00E0):
                self.iClearScreen()
            elif(self.opCode == 0x00EE):
                self.iReturnSub()
            else:
                self.iSysAddr()
        elif(self.opCode & 0xF000 == 0x1000):
            self.iJpnAddr()
        elif(self.opCode & 0xF000 == 0x2000):
            self.iCallAddr()
        elif(self.opCode & 0xF000 == 0x3000):
            self.iSeBySkip()
        elif(self.opCode & 0xF000 == 0x4000):
            self.iSneSkip()
        elif(self.opCode & 0xF000 == 0x5000):
            self.iSeVySkip()
        elif(self.opCode & 0xF000 == 0x6000):
            self.iSetVxBy()
        elif(self.opCode & 0xF000 == 0x7000):
            self.iAddVxBy()
        elif(self.opCode & 0xF000 == 0x8000):
            if(self.opCode & 0x000F == 0x0000):
                self.iSetVxVy()
            elif(self.opCode & 0x000F == 0x0001):
                self.iSetVxOVy()
            elif(self.opCode & 0x000F == 0x0002):
                self.iSetVxAVy()
            elif(self.opCode & 0x000F == 0x0003):
                self.iSetVxXVy()
            elif(self.opCode & 0x000F == 0x0004):
                self.iSetVxAVy()
            elif(self.opCode & 0x000F == 0x0005):
                self.iSetVxSVy()
            elif(self.opCode & 0x000F == 0x0006):
                self.iSHRVxVy()
            elif(self.opCode & 0x000F == 0x0007):
                self.iSetVySVx()
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
            

    def iClearScreen(self):
        print("Running iClearScreen...")

    def iReturnSub(self):
        print("Running iReturnSub...")

    def iSysAddr(self):
        print("Running iSysAddr...")

    def iJpnAddr(self):
        print("Running iJpnAddr...")

    def iCallAddr(self):
        print("Running iCallAddr...")

    def iSeBySkip(self):
        print("Running iSeBySkip...")

    def iSneSkip(self):
        print("Running iSneSkip...")

    def iSeVySkip(self):
        print("Running iSeVySkip...")

    def iSetVxBy(self):
        print("Running iSetVxBy...")

    def iAddVxBy(self):
        print("Running iAddVxBy...")

    def iSetVxVy(self):
        print("Running iSetVxVy...")

    def iSetVxOVy(self):
        print("Running iSetVxOVy...")

    def iSetVxXVy(self):
        print("Running iSetVxXVy...")

    def iSetVxAVy(self):
        print("Running iSetVxAVy...")

    def iSetVxSVy(self):
        print("Running iSetVxSVy...")

    def iSHRVxVy(self):
        print("Running iSHRVxVy...")

    def iSetVySVx(self):
        print("Running iSetVySVx...")

    def iSHLVxVy(self):
        print("Running iSHLVxVy...")

    def iSNEVxVy(self):
        print("Running iSNEVxVy...")

    def iLDIndex(self):
        print("Running iLDIndex...")

    def iJpVAddr(self):
        print("Running iJpVAddr...")

    def iSetVxRand(self):
        print("Running iSetVxRand...")

    def iDisplayBy(self):
        print("Running iDisplayBy...")

    def iSkipVxIs(self):
        print("Running iSkipVxIs...")

    def iSkipVxIsN(self):
        print("Running iSkipVxIsN...")

    def iSetVxDT(self):
        print("Running iSetVxDT...")

    def iWaitKey(self):
        print("Running iWaitKey...")

    def iSetDelay(self):
        print("Running iSetDelay...")

    def iSetSound(self):
        print("Running iSetSound...")

    def iSetVxI(self):
        print("Running iSetVxI...")

    def iSetISprite(self):
        print("Running iSetISprite...")

    def iStoreBCD(self):
        print("Running iStoreBCD...")

    def iStoreV0Vx(self):
        print("Running iStoreV0Vx...")

    def iReadV0Vx(self):
        print("Running iReadV0Vx...")