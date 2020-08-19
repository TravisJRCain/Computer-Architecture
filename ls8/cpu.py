"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0 
        # self.reg[0] = 0xF4

    def load(self, filename=None):
        """Load a program into memory."""

        # For now, we've just hardcoded a program:
        address = 0

        if filename:
            with open(filename) as f:
                for line in f:
                    value = line.split('#')[0].strip()
                    if value == "":
                        continue

                    # else:
                    instruction = int(value, 2)
                    self.ram[address] = instruction
                    address += 1

        else:
            for address, instruction in enumerate(program):
                self.ram[address] = instruction
                # return print


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

    def run(self):
        """Run the CPU."""

        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        ADD = 0b10100000
        CALL = 0b01010000
        RET = 0b00010001
        NOP = 0b00000000
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110
        
        SP = 7
        
        running = True

        while running:
            ir = self.ram[self.pc]

            oper_a = self.ram[self.pc + 1]
            oper_b = self.ram[self.pc + 2]

            if ir == HLT:
                running = False
                self.pc += 1

            elif ir == LDI:
                self.reg[oper_a] = oper_b
                self.pc += 3

            elif ir == PRN:
                print(self.reg[oper_a])
                self.pc += 2

            elif ir == MUL:
                product = self.reg[oper_a] * self.reg[oper_b]
                self.reg[oper_a] = product
                self.pc += 3

            elif ir == PUSH:
                self.reg[SP] -= 1
                self.ram_write(self.reg[oper_a], self.reg[SP])
                self.pc += 2

            elif ir == POP:
                value = self.ram_read(self.reg[SP])
                self.reg[oper_a] = value
                self.reg[SP] += 1
                self.pc += 2

            elif ir == ADD:
                add = self.reg[oper_a] + self.reg[oper_b]
                self.reg[oper_a] = add
                self.pc += 3

            elif ir == NOP:
                self.pc += 1
                continue

            elif ir == CALL:
                self.reg[SP] -= 1
                self.ram_write(self.pc + 2, self.reg[SP])

            elif ir == RET:
                self.pc = self.ram[self.reg[SP]]
                self.reg[SP] += 1

            elif ir == CMP:
                self.alu("CMP", oper_a, oper_b)
                self.pc += 3

            elif ir == JMP:
                self.pc == self.reg[oper_a]
                break

            elif ir == JEQ:
                if (self.flag & HLT) == 1:
                    self.pc = self.reg[oper_a]
                else:
                    self.pc += 2

            elif ir == JNE:
                if (self.flag & HLT) == 0:
                    self.pc = self.reg[oper_a]
                else:
                    self.pc += 2

            else:
                print(f"Unknown instructions {ir} at address {self.pc}" )
                self.pc += 1

            ###### TEST ########

if __name__ == '__main__':
    LS8 = CPU()
    LS8.load()
    for i in range(9):
        print(LS8.ram_read(i))

    LS8.ram_write(0, 15)

    print('\n')
    print(LS8.ram_read(0))
    print('\n')
